<template>
    <b-container fluid>
		<b-row>
            <b-col class="info text-center">
                <h1>{{message}}</h1>
                <div :key="timerKey">
                    <h3 class="mt-4">Time left: <strong>{{ this.booking.displayTime }}</strong></h3>
                </div>
                <div class="controls">
                    <p class="h2 mb-3">Status: <strong>{{containerState.Status}}</strong></p>
                    <b-form-checkbox class="h3 mb-3" v-model="freshImage" name="check-button" switch size="lg" :disabled="!containerState.disconnected">
                        Use fresh
                    </b-form-checkbox>
                    <b-button class="mr-2" variant="success" size="lg" :disabled="containerState.running" @click="startContainer">Start</b-button>
                    <b-button class="mr-2" variant="warning" size="lg" :disabled="containerState.inactive" @click="stopContainer">Stop</b-button>
                    <b-button class="mr-2" :href="vnc_uri" variant="primary" :disabled="containerState.inactive" target="_blank" size="lg">Connect</b-button>
                    <b-button class="ml-5" variant="info" size="md" :disabled="!containerState.exited" @click="commitContainer">Save workspace</b-button>
                    <b-button class="ml-2" variant="danger" size="md" :disabled="!containerState.exited" @click="removeContainer">Delete workspace</b-button>
                    <b-button v-if="!is_sim" class="ml-2" variant="dark" size="sm" @click="raiseIssue">HELP</b-button>
                </div>
            </b-col>
            <b-col>
                
            </b-col>
        </b-row>
        <b-row>
            <b-button class="ml-2 yield" variant="light" size="md" @click="yieldSession">Yield slot</b-button>  
        </b-row>
        <div class="room">
            <div v-if="!is_sim" class="room-items">
                <b-card class="text-center mt-4" style="max-width: 12vw" :img-src="require('../assets/camera.png')">
                    <b-button>Link to camera</b-button>
                </b-card>
                <b-img style="max-width: 20vw" :src="require('../assets/robotont.png')"></b-img>
            </div>
        </div>
        <div class="session">
            <Desktop :source="vnc_uri" />
        </div>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getCountdown } from '../util/helpers'
import Desktop from './Desktop.vue'

import axios from 'axios';
export default {
    data() {
        return {
            container: {},
            containerData: {},
            booking: {},
            freshImage: false,
            sesssionID: '',
            timerKey: 0,
            loading: true,
            started: false,
        }
    },
    components: {
        Desktop
    },
    computed: {
        ...mapGetters(["getUser"]),
        message: function() {
            const { robot_id, project, container_id } = this.container;
            if (container_id) {
                return `Your simulation environment is ready`;
            } else {
                return `You have been assigned Robotont nr. ${robot_id} at the ${project} location`;
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
            return `http://${window.location.hostname}${this.container.vnc_uri}` // change to .env
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
                this.loading = false;
            }).catch(e => {
                // With the expectation of exception 404 - container dead
                this.containerData.State = { Status: "inactive" }
                this.loading = false;
            })
        },
		startContainer: function() {
            const { slug } = this.container;
            // Always inform whether sim, the server will validate the environment if user is not an admin
            const params = new URLSearchParams([['fresh', this.freshImage], ['is_simulation', this.booking.is_simulation]]);
			axios.post(`${this.$store.state.containerAPI}/start/${slug}`, {}, {headers: this.$store.state.header, params}).then((res) => {
                const { path } = res.data
                // Update the UI
                console.log(res.data)
                this.container.vnc_uri = path;
				this.inspectContainer()
            })	
		},
		stopContainer: function() {
            const { slug } = this.container;
			axios.post(`${this.$store.state.containerAPI}/stop/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${slug} stopped`)
				this.inspectContainer()
            })	
		},
        removeContainer: function() {
            const { slug } = this.container;
			axios.post(`${this.$store.state.containerAPI}/remove/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                this.inspectContainer()
				// this.ws.send("update")
            })
		},
        commitContainer: function() {
            const { slug } = this.container;
			axios.post(`${this.$store.state.containerAPI}/commit/${slug}`, {}, {headers: this.$store.state.header}).then((res) => {
                console.log("Container successfully saved")
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
    border: 2px solid black;
}

.room-items {
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

</style>