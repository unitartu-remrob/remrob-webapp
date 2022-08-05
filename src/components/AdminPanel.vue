<template>
    <b-container fluid>
		<br><br><br>
        <b-tabs card>
			<b-tab title="Containers"  @click="switchTab(sim=false)" active>
			</b-tab>
			<b-tab title="Simtainers" @click="switchTab(sim=true)">	
			</b-tab>
		</b-tabs>
		<div class="loader" v-if="!this.is_loaded"><b-spinner class="spinner" type="grow" variant="info"></b-spinner></div>
		<b-table striped v-else :items="containerStatus" :fields="fields">
			<template v-slot:cell(status)="{ item: { running, disconnected } }">
				<CircleFill :variant="running ? 'success' : disconnected ? 'danger' : 'warning'" font-scale="1.5" />
			</template>
			<template v-slot:cell(user)="{ item: { user } }">
				<div v-if="user.isActive" class="d-flex align-items-center">
					<div class="mr-2">{{user.displayTime}}</div>
					<PersonFill font-scale="3" />
				</div>	
			</template>
			<template v-slot:cell(alarm)="{ item: { issue, id } }">
				<Exclamation variant="warning" v-if="issue" @click="clearIssue(id)" font-scale="2"/>
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
import axios from 'axios';
export default {
    data() {
        return {
            inventory: [],
			fields: [
                { key: "id", label: "Container ID", tdClass: 'align-middle', thClass: "", },
				{ key: "user", label: "", tdClass: 'align-middle text-center', thClass: "", },
				{ key: "alarm", label: "", tdClass: 'align-middle', thClass: "", },
                { key: "status", label: "State", tdClass: 'align-middle text-center', thClass: "text-center", },
				{ key: "ip", label: "IP address", tdClass: 'align-middle', thClass: "", },
				{ key: "uptime", label: "Uptime", tdClass: 'align-middle', thClass: "", },
				{ key: "cpu", label: "%CPU", tdClass: 'align-middle', thClass: "", },
				{ key: "actions", label: "", thClass: 'text-center'},
				{ key: "connection", label: "", tdClass: 'text-left', thClass: "text-center"},
            ],
			containerList: [],
			pollInterval: null,
			is_sim: false,
			is_loaded: false,
			ws: null
        }
    },   
    computed: {
        ...mapGetters(["getUser"]),
		containerStatus: function() {
			const items = this.containerList.map(container => {
				const { data, slug, booking: { end_time, issue } } = container;
				let Status,
					StartedAt,
					IPAddress

				if (data === 404) {
					Status = "inactive";
				} else {
					({ Status, StartedAt } = data.State);
					const network = Object.keys(data.NetworkSettings.Networks)[0];
					({ IPAddress } = data.NetworkSettings.Networks[network]) // what is this abomination :D
				}
				const running = (Status === "running"); // => stop active
				const disconnected = (Status === "inactive"); // remove && start active
				const inactive = (Status === "exited" || disconnected); // start active

				return {
					running, disconnected, inactive,
					ip: IPAddress,
					uptime: !inactive ? getUptime(StartedAt) : '-',
					status: Status,
					cpu: data.cpu_percent,
					vnc_uri: `http://localhost${data.vnc_uri}`, // TODO: change to .env, can add &view_only=true for spying
					id: slug,
					user: getTimeLeft(end_time),
					issue
				}
			})
			return items
		}
    },
    methods: { 
		startContainer: function(id) {
			const params = new URLSearchParams([['is_simulation', this.is_sim], ['fresh', true]]);
			axios.post(`${this.$store.state.containerAPI}/start/${id}`, {}, {headers: this.$store.state.header, params}).then((res) => {
				// this.ws.send("update") // crashes the connection ??
				console.log('something')
            })	
		},
		stopContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/stop/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${id} stopped`)
				// this.ws.send("update")
            })	
		},
		removeContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/remove/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				// this.ws.send("update")
            })
		},
		clearIssue: function(id) {
			axios.put(`${this.$store.state.baseURL}/inventory/${id}`, { issue: false }, {headers: this.$store.state.header}).then((res) => {
				// this.ws.send("update")
            })
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
			const ws = new WebSocket(`ws://localhost/containers/live/${endpoint}`) // TODO: add cookie auth, headers not available
			ws.onmessage = (event) => {
				const results = JSON.parse(event.data);
				console.log("PARSED", results)
				const data = results.map(({ slug, status, value, booking }) => {
					return {
						slug,
						booking,
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
		}
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
		this.connectWs()
    },
	beforeDestroy() {  
		this.ws.close()
    }
}
</script>

<style scoped>
.loader {
	height: 50vh;
	display: flex;
	justify-content: center;
	align-items: center;
}
.spinner {
	width: 6rem;
	height: 6rem;
}
</style>