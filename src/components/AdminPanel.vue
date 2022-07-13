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
				// "id": inv.id,
				// "robot_id": inv.robot_id,
				// "slug": inv.slug,
				// "title": f"Robotont-{inv.robot_id}",
				// "status": inv.status,
				// "project": inv.project,
				// "vnc_uri": inv.vnc_uri
        getInventory: function() {
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
				this.inventory.forEach(({robot_id, slug, vnc_uri}) => {
					this.connections[slug] = {
						// Change to .env later
						id: robot_id,
						vnc_uri: `http://localhost${vnc_uri}`
					}
				})
				this.listContainers()
            })			
        },
		listContainers: async function() {
			const calls = this.inventory.map(({ slug }) => {
				return axios.get(`${this.$store.state.containerAPI}/inspect/${slug}`, {headers: this.$store.state.header})
			});
			const results = await Promise.allSettled(calls)
			const data = this.inventory.map(({ slug }, index) => {
				return {
					id: slug,
					data: (results[index].status === 'fulfilled') 
						?  results[index].value.data
						:  404
				}
			})
			console.log(data)
			this.containerList = data
        },
		startContainer: function(c) {
			// robot_id required to update DB entry on the backend, slug used to start container
			const robot_id = this.connections[c.id].id
			axios.post(`${this.$store.state.containerAPI}/start/${robot_id}`, {slug: c.id}, {headers: this.$store.state.header}).then((res) => {
                const { path } = res.data
				// Update the UI
				this.connections[c.id].vnc_uri = `http://localhost${path}`;
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
		}
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.getInventory()	
    },
	mounted() {
		//this.pollInterval = setInterval(() => this.listContainers(), 5000)
	},
	// Only hook that triggered for interval clearance (?)
	beforeRouteLeave(to, from, next) {
		//clearInterval(this.pollInterval)
		next()
	}
	
}
</script>

<style lang="scss" scoped>

</style>