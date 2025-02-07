<template>
    <b-container fluid>
        <div class="bg-main"
        :class="isSim ? 'vr-cell' : 'bg-cell'"></div>
        <!-- <b-modal ok-title="Confirm" @ok="commitContainer" title="Save session?" id="commit-modal">
            <h4>This will overwrite any previous save</h4>
        </b-modal> -->
        <div class="loader" v-if="!this.isLoaded"><b-spinner style="width: 5rem; height: 5rem;" type="grow" variant="info"></b-spinner></div>
		<b-row v-if="this.isLoaded">``
            <b-col class="info text-center">
                <h2>{{message}}</h2>
                <div :key="timerKey">
                    <h3 class="mt-4">Time left: <strong>{{ this.booking.displayTime }}</strong></h3>
                </div>
                <div class="controls">
                    <p class="h3 mb-4">Session status: <strong>{{containerState.Status}}</strong></p>
                    <!-- <b-form-checkbox class="h3 mb-3" v-model="freshImage" name="check-button" switch size="lg" :disabled="!containerState.disconnected">
                        Use fresh
                    </b-form-checkbox> -->
                    <b-button class="mr-2" variant="success" size="lg" :disabled="containerState.running" @click="startContainer">
                        <b-spinner v-if="starting" small></b-spinner>
                        Start session
                    </b-button>
                    <b-button class="mr-3" :href="vnc_uri" variant="primary" :disabled="containerState.inactive" target="_blank" size="lg">
                        <Link font-scale="1" />
                        Connect to session!
                    </b-button>
                    <b-button class="mr-2" variant="warning" size="md" :disabled="containerState.inactive" @click="stopContainer">
                        <b-spinner v-if="stopping" small></b-spinner>
                        Stop
                    </b-button>
                    <b-button class="mr-3" variant="danger" size="md" :disabled="!containerState.exited" @click="$bvModal.show('restart-modal')">
                        <b-spinner v-if="purging" small></b-spinner>
                        Delete
                    </b-button>
                    <!-- <b-button class="ml-5" variant="info" size="md" :disabled="!containerState.exited" @click="$bvModal.show('commit-modal')">
                        <b-spinner v-if="saving" small></b-spinner>
                        Save environment
                    </b-button> -->
                </div>

            </b-col>
            <b-col>
                
            </b-col>
        </b-row>
        <b-row class="room" v-if="this.isLoaded">
            <b-alert :show="dismissCountDown" dismissible variant="success" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{successMessage}}</b-alert>
            <div v-if="!isSim" class="room-items">
                <!-- <iframe class="camera-stream"
                    :src="`/cam/webrtcstreamer.html?video=Remrob%20field%20%23${this.container.cell}&options=rtptransport%3Dtcp%26timeout%3D60`">
                </iframe> -->
                <RobotStatus :robotID="this.container.robot_id"/>
            </div>
            <div v-else class="simbot">
                <b-img :src="require('@/assets/robotont-sim.png')"></b-img>
            </div>
        </b-row>
        <div class="session" v-if="this.isLoaded" :style="isSim ? 'top: 7rem;' : ''">
            <Desktop :started="started" :source="vnc_uri" />
        </div>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getCountdown } from '@/util/helpers'
import Desktop from './Desktop.vue'
import RobotStatus from './RobotStatus.vue'
import { rootURL } from "@/util/api";

export default {
    data() {
        return {
            container: {},
            containerData: {},
            booking: {},
            freshImage: false,
            sesssionID: '',
            isLoaded: false,
            timerKey: 0,
            loading: true,
            saving: false,
            starting: false,
            started: false,
            stopping: false,
            submitting: false,
            purging: false,
            successMessage: null,
            dismissCountDown: 0,
            dismissSec: 3,
            showAlert: false,
        }
    },
    components: {
        Desktop,
        RobotStatus
    },
    computed: {
        ...mapGetters(["getUser"]),
        message: function() {
            const { robot_id, container_id } = this.container;
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
            return `${rootURL}${this.container.vnc_uri}`;
        },
        isSim: function() {
            return this.booking.is_simulation;
        }
    },
    methods: {
		inspectContainer: function() {
            const { slug } = this.container;
            this.loading = true;
            this.$api.get(`/containers/inspect/${slug}`).then((res) => {
                this.containerData = res.data
                const { status } = this.containerData;
                setTimeout(() => {
                    this.started = (status === "exited" || status === "running");
                }, 500)
                this.loading = false;
            }).catch(e => {
                // With the expectation of exception 404 - container dead
                console.log("Caught inactive")
                this.containerData = { status: "inactive" }
                this.loading = false;
            })
        },
		startContainer: function() {
            const { slug } = this.container;
            this.starting = true;
            // Always inform whether sim, the server will validate the environment if user is not an admin
            const params = new URLSearchParams([['is_simulation', this.booking.is_simulation]]);
            this.$api.post(`/containers/start/${slug}`, {}, {params}).then((res) => {
                const { path } = res.data
                // Update the UI
                this.container.vnc_uri = path;
				this.inspectContainer()
                this.starting = false;
            })	
		},
		stopContainer: function() {
            const { slug } = this.container;
            this.stopping = true;
			this.$api.post(`/containers/stop/${slug}`).then((res) => {
				console.log(`${slug} stopped`)
                this.stopping = false;
				this.inspectContainer()
            })	
		},
        // commitContainer: function() {
        //     const { slug } = this.container;
        //     this.saving = true;
		// 	this.$api.post(`/containers/commit/${slug}`).then((res) => {
        //         console.log("Container successfully saved")
        //         this.saving = false;
        //     })
		// },
        countDownChanged(dismissCountDown) {
            this.dismissCountDown = dismissCountDown
        },
        getBookingInfo: function() {
            const params = new URLSearchParams([['booking', this.sesssionID]]);
            this.$api.get(`/api/v1/bookings/${this.getUser.user_id}`, { params }).then((res) => {
                this.booking = res.data.user_bookings[0]
                console.log("Active booking", this.booking)
                // Assign ourselves a container:
                this.requestContainer();
            }).catch(_ => {
                // 404 redirect
                this.$router.push({ name: "404" })
             });
        },
        requestContainer: function() {
            this.$api.get(`/containers/assign`).then((res) => {
                console.log("Assigned container", res.data)
                this.isLoaded = true;
                this.container = res.data
                this.inspectContainer()
            }).catch(e => {
                console.log("Failed to assign a container")
                if (e.response.status == 403) {
                    this.$router.push({ name: "403" })
                }
             });
        },
        updateTime() {
            const { start, end } = this.booking;
            const time = getCountdown(start, end);
            this.booking = Object.assign(this.booking, time)
            this.timerKey += 1;
        }
    },
    created() {
        this.sesssionID = this.$route.params.session;
        // Retrieve data about the specific booking being accessed
        this.getBookingInfo()
    },
	mounted() {
        this.timer = setInterval(this.updateTime, 1000);
	},
	beforeDestroy() {  
        clearInterval(this.timer);
    },
}
</script>

<style scoped>
.info {
    position: absolute;
    margin-top: 4%;
    margin-left: 7.3%;
    padding: 3rem 1.5rem;
    background: white;
    border-radius: 1.2rem;
    border: 2px solid rgb(22, 20, 20);
    max-width: 42%;
}
.controls {
    margin-top: 2rem;
}
.session {
    /* This styling is a mess */
    position: fixed;
    transform: translateX(29rem) scale(0.58);
    right: 6rem;
    top: 4rem;
    left: 0;
    bottom: 0;
}

.vr-cell {
    background-image: url('../../assets/mesh_bg.jpg');
}

.simbot {
    position: fixed;
    left: 15%;
    top: 70%;
}

.simbot img {
    width: 110%;
    height: auto;
}

.keyboard {
    position: fixed;
    right: 35%;
    bottom: -25%;
    width: 40%;
    height: auto;
    transform: skew(-32deg, 16deg);
    z-index: 2;
    opacity: 0.85;
}

.room {
    /* height: 20%; */
    margin: 2rem 4rem;
    /* padding-bottom: 10rem; */
    width: 45%;
    position: absolute;
    left: 17%;
    top: 62%;
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