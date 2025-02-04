<template>
    <b-container fluid class="bg-white mt-4" style="max-width: 95%; margin: auto; padding: 0.75rem 1rem; border-radius: 0.5rem">
		<div class="bg-main"></div>
        <b-tabs card>
			<b-tab title="Containers"  @click="switchTab(sim=false)" active>
			</b-tab>
			<b-tab title="Simtainers" @click="switchTab(sim=true)">
			</b-tab>
		</b-tabs>
		<div class="loader" v-if="!this.is_loaded"><b-spinner style="width: 5rem; height: 5rem;" type="grow" variant="info"></b-spinner></div>
		<b-table striped v-else :items="containerStatus" :fields="filteredFields">
			<template v-slot:cell(status)="{ item: { running, disconnected } }">
				<CircleFill :variant="running ? 'success' : disconnected ? 'danger' : 'warning'" font-scale="1.5" />
			</template>
			<template v-slot:cell(robotStatus)="{ item: { robot_status } }">
				<div v-if="true" class="d-flex align-items-center justify-content-center">
					<Broadcast font-scale="2" :variant="robot_status ? 'success' : 'danger'"/>
				</div>
			</template>
			<template v-slot:cell(user)="{ item: { user, user_time } }">
				<div v-if="user_time.isActive" class="d-flex align-items-center">
					<div class="mr-2">{{user_time.displayTime}}</div>
					<PersonFill font-scale="3" />
					<div class="ml-2">{{user}}</div>
				</div>
			</template>
			<template v-slot:cell(actions)="{ item: { running, inactive, disconnected, id } }">
				<b-button class="mr-2" variant="success" :disabled="running" @click="startContainer(id)">Start</b-button>
				<b-button class="mr-2" variant="warning" :disabled="inactive" @click="stopContainer(id)">Stop</b-button>
				<b-button class="mr-2" variant="danger" :disabled="disconnected || running" @click="removeContainer(id)">Remove</b-button>
			</template>
			<template v-slot:cell(connection)="{ item: { inactive, vnc_uri } }">
				<b-button variant="primary" :disabled="inactive" target="_blank" :href="vnc_uri">Connect</b-button>
			</template>
		</b-table>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { getUptime, getTimeLeft } from '../util/helpers'
import { wsRootURL, rootURL } from "@/util/api";
import useSound from 'vue-use-sound'
import userJoinSound from "../assets/sound/start.wav";
import userLeaveSound from "../assets/sound/boop.mp3";

export default {
    data() {
        return {
            inventory: [],
			fields: [
                { key: "id", label: "Container ID", tdClass: 'align-middle', thClass: "", },
				{ key: "robotStatus", label: "Robot status", tdClass: 'align-middle', thClass: "text-center", },
				{ key: "user", label: "", tdClass: 'align-middle text-center', thClass: "", },
				{ key: "alarm", label: "", tdClass: 'align-middle', thClass: "", },
				{ key: "ip", label: "Container IP", tdClass: 'align-middle', thClass: "", },
				{ key: "uptime", label: "Uptime", tdClass: 'align-middle', thClass: "", },
				{ key: "cpu", label: "%CPU", tdClass: 'align-middle', thClass: "", },
				{ key: "actions", label: "", thClass: 'text-center'},
				{ key: "status", label: "Container status", tdClass: 'align-middle text-center', thClass: "text-center", },
				{ key: "connection", label: "", tdClass: 'text-left', thClass: "text-center"},
            ],
			containerList: [],
			containerState: {},
			pollInterval: null,
			is_sim: false,
			is_loaded: false,
			ws: null
        }
    },
    computed: {
        ...mapGetters(["getUser"]),
		filteredFields: function () {
			return this.fields.filter(field => {
				if (this.is_sim) {
					// return those that are not status
					return field.key !== 'robotStatus'
				} else {
					return true
				}
			})
		},
		containerStatus: function() {
			const items = this.containerList.map(container => {
				const { data, slug, robot_status, booking: { end_time, issue }, user } = container;
				let Status,
					StartedAt,
					IPAddress

				if (data === 404) {
					Status = "inactive";
				} else {
					({ Status, StartedAt } = data.State);
					const network = Object.keys(data.NetworkSettings.Networks)[0];
					({ IPAddress } = data.NetworkSettings.Networks[network])
				}
				const running = (Status === "running"); // => stop active
				const disconnected = (Status === "inactive"); // remove && start active
				const inactive = (Status === "exited" || disconnected); // start active

				this.containerState[slug] = { last: this.containerState[slug]?.current, current: running }

				return {
					id: slug,
					running, disconnected, inactive,
					ip: IPAddress,
					uptime: !inactive ? getUptime(StartedAt) : '-',
					status: Status,
					cpu: data.cpu_percent,
					vnc_uri: `${rootURL}${data.vnc_uri}`, // can add &view_only=true for spying
					user_time: getTimeLeft(end_time),
					user,
					issue,
					robot_status
				}
			})
			this.alertChange();
			
			return items
		}
    },
    methods: {
		startContainer: function(id) {
			const params = new URLSearchParams([['is_simulation', this.is_sim], ['fresh', true]]);
            this.$api.post(`/containers/start/${id}`, {}, {params}).then((res) => {
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
		switchTab: function(sim) {
			this.is_sim = sim
			this.ws.close()
			this.is_loaded = false
			this.connectWs()
		},
		connectWs: function() {
			console.log("connecting...")
			const endpoint = (this.is_sim) ? "simulation" : "physbots";
			const ws = new WebSocket(`${wsRootURL}/containers/live/${endpoint}`)
			ws.onmessage = (event) => {
				const results = JSON.parse(event.data);
				console.log("PARSED", results);
				const data = results?.map(({ robot_id, slug, status, robot_status, value, booking, user }) => {
					return {
						robot_id, slug,
						robot_status,
						booking, user,
						data: (status === 'fulfilled')
							?  value
							:  404,
					}
				});
				this.is_loaded = true
				this.containerList = data
			}
			ws.onopen = function(event) {
				console.log("Successfully connected to the websocket server")
			}
			this.ws = ws; // ref for closing
		},
		alertChange: function () {
			// compare containerState and play the sound alert if there's been a switch from true to false
			for (const [slug, state] of Object.entries(this.containerState)) {
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
		containerState: function (val) {
			console.log("containerStatus", val)
		} 
	},
    created() {
		this.connectWs()
    },
	beforeDestroy() {
		this.ws.close()
    }
}
</script>

<style scoped>

</style>