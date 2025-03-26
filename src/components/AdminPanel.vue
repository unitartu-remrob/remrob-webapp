<template>
    <b-container fluid class="bg-white mt-4" style="max-width: 95%; margin: auto; padding: 0.75rem 1rem; border-radius: 0.5rem">
		<div class="bg-main"></div>
        <b-tabs card>
			<b-tab title="Containers"  @click="switchTab(sim=false)">
			</b-tab>
			<b-tab title="Simtainers" @click="switchTab(sim=true)" active>
			</b-tab>
		</b-tabs>
		<div class="loader" v-if="!this.isLoaded"><b-spinner style="width: 5rem; height: 5rem;" variant="info"></b-spinner></div>
		<b-table striped v-else :items="containerStatus" :fields="filteredFields">
			<template v-slot:cell(image)="{ item: { image, id, disconnected } }">
                <b-form-select v-if="disconnected"
					:options="imageOptions"
					v-model="chosenImages[id]">
				</b-form-select>
				<div v-else class="ml-2">
					<b-img class="version-icon mr-2" :src="imageHandler.versionLogo(image)"></b-img>
					<span>{{ imageHandler.getImageLabel(image) }}</span>
				</div>
			</template>

			<template v-slot:cell(publicContainer)="{ item: { publicContainer } }">
				<div v-if="publicContainer" class="d-flex align-items-center justify-content-center" >
					<span style="font-size: 1.3rem">🌐</span><span class="ml-2">Public</span>
				</div>
			</template>
			
			<template v-slot:cell(robotStatus)="{ item: { robot_status } }">
				<div v-if="true" class="d-flex align-items-center justify-content-center">
					<Broadcast font-scale="2" :variant="robot_status ? 'success' : 'danger'"/>
				</div>
			</template>
			<template v-slot:cell(user)="{ item: { user, user_time } }">
				<div v-if="user_time.isActive" class="d-flex align-items-center">
					<div class="mr-2">{{ user_time.displayTime }}</div>
					<PersonFill font-scale="3" />
					<div class="ml-2">{{ user }}</div>
				</div>
			</template>
			<template v-slot:cell(actions)="{ item: { id, running, inactive, disconnected } }">
				<b-button class="mr-2" variant="success" :disabled="running" @click="startContainer(id)">Start</b-button>
				<b-button class="mr-2" variant="warning" :disabled="inactive" @click="stopContainer(id)">Stop</b-button>
				<b-button class="mr-2" variant="danger" :disabled="disconnected || running" @click="removeContainer(id)">Remove</b-button>
			</template>
			<template v-slot:cell(status)="{ item: { running, disconnected } }">
				<CircleFill :variant="running ? 'success' : disconnected ? 'danger' : 'warning'" font-scale="1.5" />
			</template>
			<template v-slot:cell(connection)="{ item: { inactive, vnc_uri } }">
				<b-button variant="primary" :disabled="inactive" target="_blank" :href="vnc_uri">Connect</b-button>
			</template>
		</b-table>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getUptime, getTimeLeft } from '@/util/helpers'
import { wsRootURL, rootURL } from "@/util/api";
import { getImageOptions } from '@/shared/getImages';
import useSound from 'vue-use-sound'
import userJoinSound from "../assets/sound/start.wav";
import userLeaveSound from "../assets/sound/boop.mp3";

export default {
    data() {
        return {
            inventory: [],
			containerList: [],
			containerState: {},

			fields: [
                { key: "id", label: "Container ID", tdClass: 'align-middle', thClass: "", },
				{ key: "image", label: "Session type", tdClass: 'align-middle'},
				{ key: "robotStatus", label: "Robot status", tdClass: 'align-middle', thClass: "text-center", },
				{ key: "publicContainer", label: "", tdClass: 'align-middle', thClass: "text-center", },
				{ key: "user", label: "", tdClass: 'align-middle text-center', thClass: "", },
				{ key: "ip", label: "Container IP", tdClass: 'align-middle', thClass: "", },
				{ key: "uptime", label: "Uptime", tdClass: 'align-middle', thClass: "", },
				{ key: "cpu", label: "%CPU", tdClass: 'align-middle', thClass: "", },
				{ key: "actions", label: "", thClass: 'text-center'},
				{ key: "status", label: "Container status", tdClass: 'align-middle text-center', thClass: "text-center", },
				{ key: "connection", label: "", tdClass: 'text-left', thClass: "text-center"},
            ],
			
			imageHandler: null,
			chosenImages: {},
			imagesAreLoaded: false,

			pollInterval: null,
			isSim: true,
			isLoaded: false,
			ws: null
        }
    },
    computed: {
        ...mapGetters(["getUser"]),
		filteredFields: function () {
			return this.fields.filter(field => {
				if (this.isSim) {
					// return those that are not status
					return !['robotStatus'].includes(field.key)
				} else {
					return !['publicContainer'].includes(field.key)
				}
			})
		},
		containerStatus: function() {
			const items = this.containerList.map(container => {
				const {
					data: {
						status,
						image,
						createdAt,
						ipAddress,
						cpu_percent
					},
					slug,
					robot_status,
					end_time,
					user,
					open_to_public,
					vnc_uri
				} = container;

				const running = (status === "running"); // => stop active
				const disconnected = (status === "inactive"); // remove && start active
				const inactive = (status === "exited" || disconnected); // start active

				this.containerState[slug] = { last: this.containerState[slug]?.current, current: running }

				return {
					id: slug,
					image,
					running, disconnected, inactive,
					ip: ipAddress,
					uptime: !inactive ? getUptime(createdAt) : '-',
					status,
					cpu: cpu_percent,
					vnc_uri: `${rootURL}${vnc_uri}`, // can add &view_only=true for spying
					user_time: getTimeLeft(end_time),
					user,
					robot_status,
					isSim: this.isSim,
					publicContainer: open_to_public
				}
			})
			this.alertChange();
			
			return items
		},
		imageOptions: function() {
			const { imageOptionsSim, imageOptionsPhysbot } = this.imageHandler;

			return this.isSim ? imageOptionsSim : imageOptionsPhysbot;
		},
    },
    methods: {
		switchTab: function(isSim) {
			this.isSim = isSim
			this.ws.close()
			this.isLoaded = false
			this.connectWs()
		},
		connectWs: function() {
			console.log("connecting...")
			const endpoint = (this.isSim) ? "simulation" : "physbots";
			this.ws = new WebSocket(`${wsRootURL}/containers/live/${endpoint}`)

			this.ws.onmessage = (event) => {
				const results = JSON.parse(event.data);
				const data = results?.map(({ status, value, ...restOfProps }) => {
					return {
						data: (status === 'fulfilled')
							?  value
							:  {
								status: 'inactive'
							},
						...restOfProps,
					}
				});
				this.isLoaded = true
				this.containerList = data
			}
			this.ws.onopen = function() {
				console.log("Successfully connected to the websocket server")
			}
		},
		getImageVariants: function() {
			getImageOptions().then(imageHandler => {
				this.imageHandler = imageHandler
				this.imagesAreLoaded = true
			}).catch(err => {
				console.error("Error getting images", err)
			})
		},
		updateImageVariants: function() {
			const { defaultImageSim, defaultImagePhysbot } = this.imageHandler;

			console.log("updating with default images", defaultImageSim, defaultImagePhysbot)
			console.log("chosenImages", this.containerList, this.chosenImages)

			this.containerList.forEach(container => {
				this.chosenImages[container.slug] = this.isSim ? defaultImageSim : defaultImagePhysbot;
			})
		},
		startContainer: function(id) {
			const queryParams = new URLSearchParams([['is_simulation', this.isSim]]);
			const body = {
				rosVersion: this.imageHandler.getImageRosVersion(this.chosenImages[id]),
				imageTag: this.chosenImages[id]
			}

            this.$api.post(`/containers/start/${id}`, body, { params: queryParams }).then((res) => {
                // this.ws.send("update") // crashes the connection ??
            })
		},
		stopContainer: function(id) {
            this.$api.post(`/containers/stop/${id}`, {}).then((_) => {
				console.log(`${id} stopped`)
            })
		},
		removeContainer: function(id) {
			this.$api.post(`/containers/remove/${id}`, {});
		},
		alertChange: function () {
			// compare containerState and play the sound alert if there's been a switch from true to false
			for (const state of Object.values(this.containerState)) {
				if (state.last === true && state.current === false) {
					this.stopSound();
				} else if (state.last === false && state.current === true) {
					this.startSound();
				}
			}
		},
    },
	setup() {
		const [startSound] = useSound(userJoinSound);
		const [stopSound] = useSound(userLeaveSound);
		return { startSound, stopSound }
	},
	watch: {
		imagesAreLoaded(val) {
			if (val) {
				// set default images for each container
				this.updateImageVariants();
			}
		},
		isLoaded(val) {
			if (val) {
				this.updateImageVariants()
			}
		}
	},
    created() {
		this.connectWs()
		this.getImageVariants()
    },
	beforeDestroy() {
		this.ws.close()
    }
}
</script>

<style scoped>

.version-icon {
	width: 3rem;
	height: 3rem;
	object-fit: cover;
}
</style>