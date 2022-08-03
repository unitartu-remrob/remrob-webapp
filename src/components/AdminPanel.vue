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
import { getUptime } from '../util/helpers'
import axios from 'axios';
export default {
    data() {
        return {
            inventory: [],
			fields: [
                { key: "id", label: "Container ID" },
                { key: "status", label: "State" },
				{ key: "ip", label: "IP address" },
				{ key: "uptime", label: "Uptime" },
				{ key: "cpu", label: "%CPU" },
				"actions",
				"connection"
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
				const { data, slug } = container;
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
					id: slug
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
		switchTab: function(sim) {
			this.is_sim = sim
			this.ws.close()
			this.is_loaded = false
			this.connectWs()
		},
		connectWs: function() {
			console.log("connecting...")
			const endpoint = (this.is_sim) ? "simulation" : "physbots";
			const ws = new WebSocket(`ws://localhost:9000/api/container/live/${endpoint}`) // TODO: add cookie auth, headers not available
			ws.onmessage = (event) => {
				const results = JSON.parse(event.data);
				console.log("PARSED", results)
				const data = results.map(({ slug, status, value }) => {
					return {
						slug,
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