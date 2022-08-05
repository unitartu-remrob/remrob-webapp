<template>
    <b-container fluid>
		<br><br><br>
		<b-row>
            <b-col class="text-center">
                <p>SESSION {{ this.$route.params.session }} HERE</p>
                <p>{{message}}</p>
                <div :key="timerKey">
                    <p v-if="true">Time left: {{ this.booking.displayTime }}</p>
                    <p v-else>Finished</p>
                </div>
            </b-col>
        </b-row>
        <br>
        <b-card class="border text-center float-right mr-5" style="max-width: 50vw" img-fluid :img-src="require('../assets/ubuntu.png')">
            <b-button :href="vnc_uri" variant="primary" :disabled="containerState.inactive" target="_blank" size="lg">Connect</b-button>
            <b-img style="max-width: 10vw" :src="require('../assets/robotont.png')"></b-img>
        </b-card>
        <b-row>
            <b-col class="text-center mr-5">
                <p class="h2 mb-3">Status: <strong>{{containerState.Status}}</strong></p>
                <b-form-checkbox class="h3 mb-3" v-model="freshImage" name="check-button" switch size="lg" :disabled="!containerState.disconnected">
                    Use fresh
                </b-form-checkbox>
                <b-button class="mr-2" variant="success" size="lg" :disabled="containerState.running" @click="startContainer()">Start</b-button>
                <b-button class="mr-2" variant="warning" size="lg" :disabled="containerState.inactive" @click="stopContainer()">Stop</b-button>
                <b-button class="ml-5" variant="info" size="md" :disabled="!containerState.exited" @click="commitContainer()">Save workspace</b-button>
                <b-button class="ml-2" variant="danger" size="sm" :disabled="!containerState.exited" @click="removeContainer()">Delete workspace</b-button>
                <b-button class="ml-2" variant="dark" size="sm" @click="raiseIssue()">HELP</b-button>     
            </b-col>
        </b-row>
        <b-row>
            <b-col>

            </b-col>
        </b-row>
        <br><br><br>
        <b-row>
            <b-card style="max-width: 20vw" img-fluid class="text-center ml-5" :img-src="require('../assets/camera.png')">
                <b-card-text>Link to camera</b-card-text>
            </b-card>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getCountdown } from '../util/helpers'

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
            return `http://localhost${this.container.vnc_uri}` // change to .env
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
            const params = new URLSearchParams([['fresh', this.freshImage]]);
			axios.post(`${this.$store.state.containerAPI}/start/${slug}`, {}, {headers: this.$store.state.header, params}).then((res) => {
                const { path } = res.data
                // Update the UI
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
            }).catch(e => console.log(e)); // 404 redirect?
        },
        requestContainer: function() {
            axios.get(`${this.$store.state.containerAPI}/assign`, {headers: this.$store.state.header}).then((res) => {
                console.log("Assigned container", res.data)
                this.container = res.data
                this.inspectContainer()
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

<style lang="scss" scoped>

</style>