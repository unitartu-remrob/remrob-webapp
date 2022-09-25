<template>
    <b-container fluid>
        <!-- <b-modal ok-title="Confirm" @ok="removeContainer" title="Remove workspace?" id="kill-modal">
            <h4>This will remove any unsaved changes</h4>
        </b-modal> -->
        <b-modal ok-title="Confirm" @ok="yieldSession" title="Quit session" id="yield-modal">
            <h4>Are you sure you want to surrender your slot?</h4>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="commitContainer" title="Save session?" id="commit-modal">
            <h4>This will overwrite any previous save</h4>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="purgeContainer" title="Restart session?" id="restart-modal">
            <h4>This will delete any unsaved work and give you a fresh start opportunity</h4>
        </b-modal>
        <div class="loader" v-if="!this.is_loaded"><b-spinner style="width: 5rem; height: 5rem;" type="grow" variant="info"></b-spinner></div>
		<b-row v-if="this.is_loaded">
            <b-col class="info text-center">
                <h1>{{message}}</h1>
                <div :key="timerKey">
                    <h3 class="mt-4">Time left: <strong>{{ this.booking.displayTime }}</strong></h3>
                </div>
                <div class="controls">
                    <p class="h2 mb-5">Session status: <strong>{{containerState.Status}}</strong></p>
                    <!-- <b-form-checkbox class="h3 mb-3" v-model="freshImage" name="check-button" switch size="lg" :disabled="!containerState.disconnected">
                        Use fresh
                    </b-form-checkbox> -->
                    <b-button class="mr-2" variant="success" size="lg" :disabled="containerState.running" @click="startContainer">
                        <b-spinner v-if="starting" small></b-spinner>
                        Start session
                    </b-button>
                    <!-- <b-button class="mr-2" variant="warning" size="lg" :disabled="containerState.inactive" @click="stopContainer">
                        <b-spinner v-if="stopping" small></b-spinner>
                        Stop
                    </b-button> -->
                    <b-button class="mr-3" :href="vnc_uri" variant="primary" :disabled="containerState.inactive" target="_blank" size="lg">
                        <Link font-scale="1" />
                        Connect to session!
                    </b-button>
                    <b-button class="mr-3" variant="warning" size="md" :disabled="containerState.inactive" @click="$bvModal.show('restart-modal')">
                        <b-spinner v-if="purging" small></b-spinner>
                        Delete session
                    </b-button>
                    <b-button class="ml-5" variant="dark" size="lg" :disabled="containerState.inactive" @click="commitCode">
                        <b-spinner v-if="submitting" small></b-spinner>
                        Submit code
                    </b-button>                   
                    <!-- <b-button class="ml-5" variant="info" size="md" :disabled="!containerState.exited" @click="$bvModal.show('commit-modal')">
                        <b-spinner v-if="saving" small></b-spinner>
                        Save environment
                    </b-button> -->
                    <!-- <b-button class="ml-2" variant="danger" size="md" :disabled="!containerState.exited" @click="removeContainer"></b-button> -->
                    <!-- <b-button v-if="!is_sim" class="ml-2" variant="dark" size="sm" @click="raiseIssue">HELP</b-button> -->
                </div>
                
            </b-col>
            <b-col>
                
            </b-col>
        </b-row>
        <!-- <b-row v-if="this.is_loaded">
            <b-button class="ml-2 yield" variant="light" size="md" @click="$bvModal.show('yield-modal')">Yield slot</b-button>  
        </b-row> -->
        <div class="room" v-if="this.is_loaded">
            <div v-if="!is_sim" class="room-items">
                <!-- <b-card class="text-center mt-4" style="max-width: 12vw" :img-src="require('../assets/camera.png')">
                    <b-button>Link to camera</b-button>
                </b-card> -->
                <iframe class="camera-stream"
                    :src="`/cam/webrtcstreamer.html?video=Remrob%20field%20%23${this.container.cell}&options=rtptransport%3Dtcp%26timeout%3D60`">
                </iframe>
                <RobotStatus :robotID="this.container.robot_id"/>
            </div>
        </div>
        <div class="session" v-if="this.is_loaded">
            <Desktop :started="started" :source="vnc_uri" />
        </div>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getCountdown } from '../util/helpers'
import Desktop from './Desktop.vue'
import RobotStatus from './RobotStatus.vue'
import axios from 'axios';

export default {
    data() {
        return {
            container: {},
            containerData: {},
            booking: {},
            freshImage: false,
            sesssionID: '',
            is_loaded: false,
            timerKey: 0,
            loading: true,
            saving: false,
            starting: false,
            started: false,
            stopping: false,
            submitting: false,
            purging: false,
        }
    },
    components: {
        Desktop,
        RobotStatus
    },
    computed: {
        ...mapGetters(["getUser"]),
        message: function() {
            const { robot_id, project, container_id } = this.container;
            if (container_id) {
                return `Your simulation environment is ready`;
            } else {
                return `You have been assigned Robotont nr. ${robot_id}`;
            }
        },
        containerState: function() {
            if (!this.loading) {
                const { Status } = this.containerData.State;
                const running = (Status === "running");
                const disconnected = (Status === "inactive");
                const exited = (Status === "exited");
                const inactive = (exited || disconnected);

                return {
                    running, inactive, disconnected, exited, Status
                }  
            } else {
                return {}
            }
        },
        vnc_uri: function() {
            return `${this.$store.state.rootURL}${this.container.vnc_uri}`;
        },
        is_sim: function() {
            return this.booking.is_simulation;
        }
    },
    methods: {
		inspectContainer: function() {
            const { slug } = this.container;
            this.loading = true;
            axios.get(`${this.$store.state.containerAPI}/inspect/${slug}`, {headers: this.$store.state.header}).then((res) => {
                this.containerData = res.data
                const { Status } = this.containerData.State;
                setTimeout(() => {
                    this.started = (Status === "exited" || Status === "running") ? true : false;
                }, 500)
                this.loading = false;
            }).catch(e => {
                // With the expectation of exception 404 - container dead
                this.containerData.State = { Status: "inactive" }
                this.loading = false;
            })
        },
		startContainer: function() {
            const { slug } = this.container;
            this.starting = true;
            // Always inform whether sim, the server will validate the environment if user is not an admin
            const params = new URLSearchParams([['fresh', this.freshImage], ['is_simulation', this.booking.is_simulation]]);
			axios.post(`${this.$store.state.containerAPI}/start/${slug}`, {}, {headers: this.$store.state.header, params}).then((res) => {
                const { path } = res.data
                // Update the UI
                console.log(res.data)
                this.container.vnc_uri = path;
				this.inspectContainer()
                this.starting = false;
                // Artificial buffer to        
            })	
		},
		stopContainer: function() {
            const { slug } = this.container;
            this.stopping = true;
			axios.post(`${this.$store.state.containerAPI}/stop/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${slug} stopped`)
                this.stopping = false;
				this.inspectContainer()
            })	
		},
        removeContainer: function() {
            const { slug } = this.container;
			axios.post(`${this.$store.state.containerAPI}/remove/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                this.inspectContainer()
                this.started = false
				// this.ws.send("update")
            })
		},
        purgeContainer: function() {
            const { slug } = this.container;
            this.purging = true;
			axios.post(`${this.$store.state.containerAPI}/stop/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                axios.post(`${this.$store.state.containerAPI}/remove/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                    console.log(`${slug} purged`)
                    this.started = false
                    // this.ws.send("update")
                    this.purging = false;
                    this.inspectContainer()
                })
            })	
		},
        commitContainer: function() {
            const { slug } = this.container;
            this.saving = true;
			axios.post(`${this.$store.state.containerAPI}/commit/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                console.log("Container successfully saved")
                this.saving = false;
            })
		},
        commitCode: function() {
            this.submitting = true;
            // This will find the user in DB and make a push for its corresponding repository
			axios.get(`${this.$store.state.baseURL}/commit_push_jwt`, {headers: this.$store.state.header}).then((res) => {
                console.log("Code successfully pushed")
                this.submitting = false;
            })
		},
        raiseIssue: function() {
            const { slug } = this.container;
			axios.put(`${this.$store.state.baseURL}/inventory/${slug}`, { issue: true }, {headers: this.$store.state.header}).then((res) => {
                console.log("Issue submitted")
            })
		},
        getBookingInfo: function() {
            const params = new URLSearchParams([['booking', this.sesssionID]]);
            axios.get(`${this.$store.state.baseURL}/bookings/${this.getUser.user_id}`, {headers: this.$store.state.header, params}).then((res) => {
                this.booking = res.data.user_bookings[0]
                console.log("Active booking", this.booking)
                // Assign ourselves a container:
                this.requestContainer();
            }).catch(e => {
                // 404 redirect?
                this.$router.push({name: "404"})
             });
        },
        requestContainer: function() {
            axios.get(`${this.$store.state.containerAPI}/assign`, {headers: this.$store.state.header}).then((res) => {
                console.log("Assigned container", res.data)
                this.is_loaded = true;
                this.container = res.data
                this.inspectContainer()
            }).catch(e => {
                // this.$router.push({name: "UserPanel"})
             });
        },
        yieldSession: function() {
            const { slug } = this.container;   
            axios.post(`${this.$store.state.containerAPI}/yield/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                this.$router.push({ name: "Home" })
            })
        },
        updateTime() {
            const { start, end } = this.booking;
            const time = getCountdown(start, end);
            this.booking = Object.assign(this.booking, time)
            this.timerKey += 1;
        }
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.sesssionID = this.$route.params.session;
        // Retrieve data about the specific booking being accessed
        this.getBookingInfo()
    },
	mounted() {
        this.timer = setInterval(this.updateTime, 1000);
		// this.pollInterval = setInterval(() => this.inspectContainer(), 2000)
	},
	beforeDestroy() {  
        clearInterval(this.timer);
    },
}
</script>

<style scoped>
.info {
    margin-top: 8rem;
}
.controls {
    margin-top: 3rem;
}
.session {
    /* This styling is a mess */
    transform: translateX(29rem) scale(0.58);
    margin-top: -56rem;
}
.yield {
    position: absolute;
    right: 10rem;
    top: 10rem;
    font-size: 1.5rem;
    border: 2px solid rgb(201, 204, 37);
}
.room {
    height: 22rem;
    margin: 2rem 4rem;
    width: 42vw;
    /* border: 2px solid black; */
}

.room-items {
    display: flex;
    position: relative;
    justify-content: center;
    align-items: center;
    gap: 4rem;
    padding: 2rem 0;
}

.camera-stream {
    height: 18rem;
    width: 100%;
    top: 0;
}

</style>