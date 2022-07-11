<template>
    <b-container fluid>
		<br><br><br>
		<b-row>
            <b-col>
                ADMIN HERE
            </b-col>
        </b-row>
        <br><br><br><br>
        <b-row>
            <b-col>
                <b-table striped :items="containerStatus" :fields="fields">
					<template v-slot:cell(actions)="{ item }">
						<b-button class="mr-2" @click="startContainer(item)">Start</b-button>
						<b-button class="mr-2" @click="stopContainer(item)">Stop</b-button>
						<b-button class="mr-2" @click="removeContainer(item)">Remove</b-button>
					</template>
					<template v-slot:cell(connection)="{ item }">
						<b-button target="_blank" :href="connections[item.id].vnc_uri">Connect</b-button>
					</template>
				</b-table>
            </b-col>
        </b-row>

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
				"actions",
				"connection"
            ],
			robot_ids: [],
			containerList: [],
			connections: {},
			pollInterval: null
        }
    },   
    computed: {
        ...mapGetters(["getUser"]),
		containerStatus: function() {
			const items = this.containerList.map(container => {
				const { id, data } = container;
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
				const RUNNING = (Status === "running");
				const DISCONNECTED = (Status === "inactive");
				const INACTIVE = (Status === "exited" || DISCONNECTED);

				return {
					id: id,
					ip: IPAddress,
					uptime: !INACTIVE ? getUptime(StartedAt) : '-',
					status: Status
				}
			})
			console.log(items)
			return items
		}
    },
    methods: {
		lol: function(e) {
			console.log(e)
		},
        getInventory: function() {
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
				this.robot_ids = this.inventory.map(({robot_id}) => `robo-${robot_id}`)
				this.inventory.forEach(({robot_id, id, vnc_uri}) => {
					this.connections[`robo-${robot_id}`] = {
						id: id,
						vnc_uri: `http://localhost${vnc_uri}`
					}
				})
				console.log(this.connections)
				this.listContainers()
            })			
        },
		listContainers: async function() {
			const calls = this.robot_ids.map(id => {
				return axios.get(`${this.$store.state.containerAPI}/inspect/${id}`, {headers: this.$store.state.header})
			});
			const results = await Promise.allSettled(calls)
			const data = this.robot_ids.map((id, index) => {
				return {
					id: id,
					data: (results[index].status === 'fulfilled') 
						?  results[index].value.data
						: 404
				}
			})
			this.containerList = data
        },
		startContainer: function(c) {
			axios.post(`${this.$store.state.containerAPI}/start/${c.id}`, {}, {headers: this.$store.state.header}).then((res) => {
                const { path } = res.data
				// Update the UI
				this.connections[c.id].vnc_uri = `http://localhost${path}`;
				// Update the database entry
				this.updateURI(this.connections[c.id].id, path)
				console.log(path)
				this.listContainers()
            })	
		},
		stopContainer: function(c) {
			axios.post(`${this.$store.state.containerAPI}/stop/${c.id}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${c.id} stopped`)
				this.listContainers()
            })	
		},
		removeContainer: function(c) {
			axios.post(`${this.$store.state.containerAPI}/remove/${c.id}`, {}, {headers: this.$store.state.header}).then((res) => {
				this.listContainers()
            })	
		},
		updateURI: function(id, uri) {
			axios.put(`${this.$store.state.baseURL}/inventory/${id}`, { vnc_uri: uri }, {headers: this.$store.state.header}).then((res) => {
				this.listContainers()
            })	
		},
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.getInventory()	
    },
	mounted() {
		this.pollInterval = setInterval(() => this.listContainers(), 5000)
	},
	// Only hook that triggered for interval clearance (?)
	beforeRouteLeave(to, from, next) {
		clearInterval(this.pollInterval)
		next()
	}
	
}
</script>

<style lang="scss" scoped>

</style>