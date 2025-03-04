<template>
    <b-container fluid>
        <div class="bg-main"
        :class="isSim ? 'vr-cell' : 'bg-cell'"></div>
        <!-- <b-modal ok-title="Confirm" @ok="commitContainer" title="Save session?" id="commit-modal">
            <h4>This will overwrite any previous save</h4>
        </b-modal> -->
        <b-modal ok-title="Confirm" @ok="removeContainer" title="Restart session?" id="restart-modal">
            <h4>This will undo all system changes (except files stored in your catkin workspace and Submission folder)</h4>
        </b-modal>
        <div class="loader" v-if="!this.isLoaded"><b-spinner style="width: 5rem; height: 5rem;" type="grow" variant="info"></b-spinner></div>
		<b-row v-if="this.isLoaded">``
            <b-col class="info text-center" v-if="this.sessionIsActive">
                <h2>{{ message }}</h2>
                <div :key="timerKey">
                    <h3 class="mt-4">Time left: <strong>{{ this.displayTime }}</strong></h3>
                </div>
                <p class="h3 mt-4 mb-5">Session status: <strong>{{ containerState.status }}</strong></p>
                <div>
                    <strong class="image-pick-label" v-if="containerState.disconnected">
                        Pick environment:
                    </strong>
                    <b-form-select class="image-dropdown" v-if="containerState.disconnected"
                        :options="imageOptions"
                        v-model="chosenImage">
                    </b-form-select>
                    <span v-else>
                        <span class="h4 mr-3">Session type:</span>
                        <b-img class="version-icon mr-2" :src="imageHandler.versionLogo(chosenImage)"></b-img>
                        <strong style="font-size: 1.2rem">{{ imageHandler.getImageLabel(chosenImage) }}</strong>
                    </span>
                </div>

                <div class="controls p-2">                    
                    <!-- <b-form-checkbox class="h3 mb-3" v-model="freshImage" name="check-button" switch size="lg" :disabled="!containerState.disconnected">
                        Use fresh
                    </b-form-checkbox> -->
                    <b-button class="mr-2" variant="success" size="lg" :disabled="containerState.running" @click="startContainer">
                        <b-spinner v-if="starting" small></b-spinner>
                        Start session
                    </b-button>
                    <b-button class="mr-3" :href="vnc_uri" variant="primary" :disabled="containerState.inactive" target="_blank" size="lg" @click="disableDesktopIframe">
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
            <b-col class="info text-center" v-else>
                <h2 class="mb-4">Your session is over.</h2>
                <h4>See if you can book another!</h4>
                <b-button class="mt-2" variant="primary" @click="$router.push({ name: 'Booking' })">Go to booking</b-button>
            </b-col>
        </b-row>
        <b-row class="room" v-if="this.isLoaded">
            <!-- <b-alert :show="dismissCountDown" dismissible variant="success" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{successMessage}}</b-alert> -->
            <!-- <iframe class="camera-stream"
                :src="`/cam/webrtcstreamer.html?video=Remrob%20field%20%23${this.container.cell}&options=rtptransport%3Dtcp%26timeout%3D60`">
            </iframe> -->
            <div v-if="!this.isSim" class="room-items">
                <RobotStatus :robotID="this.container.robot_id"/>
            </div>
            <div v-else class="simbot">
                <b-img :src="require('@/assets/robotont-sim.png')"></b-img>
            </div>
        </b-row>
        <div class="session" v-if="this.isLoaded" :style="this.isSim ? 'top: 7rem;' : ''">
            <Desktop :started="started && !hasConnected" :source="vnc_uri" />
        </div>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getCountdown } from '@/util/helpers'
import Desktop from './Desktop.vue'
import RobotStatus from './RobotStatus.vue'
import { rootURL } from "@/util/api";
import { getImageOptions } from '../../shared/getImages';

export default {
    data() {
        return {
            container: {},
            containerData: {},
            booking: {},
            isSim: null,
            displayTime: '',
            sessionIsActive: true,

            imageHandler: null,
            images: [],
			chosenImage: '',

            sesssionID: '',
            isLoaded: false,
            hasConnected: false,
            timerKey: 0,

            loading: true,

            saving: false,
            starting: false,
            started: false,
            stopping: false,
            submitting: false,
            purging: false,

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
            const { robot_id } = this.container;
            if (robot_id !== undefined) {
                return `You have been assigned Robotont nr. ${robot_id}`;
            } else {
                return `Your simulation environment is ready`;
            }
        },
        containerState: function() {
            if (!this.loading) {
                const { status } = this.containerData;
                const running = (status === "running");
                const disconnected = (status === "inactive");
                const exited = (status === "exited");
                const inactive = (exited || disconnected);

                return {
                    running, inactive, disconnected, exited, status
                }  
            } else {
                return {}
            }
        },
        vnc_uri: function() {
            return `${rootURL}${this.container.vnc_uri}`;
        },
        imageOptions: function() {
            return this.images.map(({ imageTag, label }) => {
                return { value: imageTag, text: label }
            })
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

            const image = this.chosenImage;

            const body = {
                rosVersion: this.imageHandler.getImageRosVersion(image),
                imageTag: image,
            }

            // Always inform whether sim, the server will validate the environment if user is not an admin
            const params = new URLSearchParams([['is_simulation', this.booking.is_simulation]]);

            this.$api.post(`/containers/start/${slug}`, body, { params }).then((res) => {
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
            this.hasConnected = false;
		},
        removeContainer: function() {
            const { slug } = this.container;
			this.$api.post(`/containers/remove/${slug}`).then((res) => {
                this.inspectContainer()
                this.started = false
				// this.ws.send("update")
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
        // countDownChanged(dismissCountDown) {
        //     this.dismissCountDown = dismissCountDown
        // },
        disableDesktopIframe: function() {
            this.hasConnected = true;
        },
        getBookingInfo: function() {
            const params = new URLSearchParams([['booking', this.sesssionID]]);
            this.$api.get(`/api/v1/bookings/${this.getUser.user_id}`, { params }).then((res) => {
                this.booking = res.data.user_bookings[0]
                this.isSim = this.booking.is_simulation;

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
                if (e.response.status == 403) {
                    this.$router.push({ name: "403" })
                }
             });
        },
        updateTime() {
            const { start, end } = this.booking;
            const sessionTime = getCountdown(start, end);

            this.displayTime = sessionTime.displayTime;
            this.sessionIsActive = sessionTime.isActive;
            this.timerKey += 1;
        },
        getImageVariants: function() {
			getImageOptions().then(imageHandler => {
				this.imageHandler = imageHandler
                const { defaultImageSim, defaultImagePhysbot, images } = imageHandler;

                this.images = images;
                this.chosenImage = this.isSim ? defaultImageSim : defaultImagePhysbot;
			}).catch(err => {
				console.error("Error getting images", err)
			})
		},
    },
    created () {
        this.sesssionID = this.$route.params.session;
        // Retrieve data about the specific booking being accessed
        this.getBookingInfo();
        this.getImageVariants();
    },
	mounted() {
        this.timer = setInterval(this.updateTime, 1000);
	},
    watch: {
        isSim: function(val) {
            if (!val) {
                this.images = this.images.filter(image => !image.simulationExclusive);
            }
        }
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

@media screen and (min-width: 2000px) {
    .info {
        max-width: 34%;
    }
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


@media screen and (min-width: 2000px) {
    .simbot img {
        width: 130%;
    }
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

.image-dropdown {
    max-width: 40%;
    position: relative;
}

.image-pick-label {
    font-size: 1.2rem;
    /* color: rgb(174, 196, 202); */
    margin-top: 1rem;
    margin-right: 1rem;
}

.version-icon {
	width: 4rem;
	height: 4rem;
	object-fit: cover;
}

.camera-stream {
    height: 18rem;
    width: 100%;
    top: 0;
}

</style>