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
					<template v-slot:cell(actions)="{ item: { running, inactive, disconnected, id } }">
						<b-button class="mr-2" variant="success" :disabled="running" @click="startContainer(id)">Start</b-button>
						<b-button class="mr-2" variant="warning" :disabled="inactive" @click="stopContainer(id)">Stop</b-button>
						<b-button class="mr-2" variant="danger" :disabled="disconnected || running" @click="removeContainer(id)">Remove</b-button>
					</template>
					<template v-slot:cell(connection)="{ item: { inactive, vnc_uri } }">
						<b-button variant="primary" :disabled="inactive" target="_blank" :href="vnc_uri">Connect</b-button>
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
				{ key: "cpu", label: "%CPU" },
				"actions",
				"connection"
            ],
			containerList: [],
			pollInterval: null
        }
    },   
    computed: {
        ...mapGetters(["getUser"]),
		containerStatus: function() {
			const items = this.containerList.map(container => {
				const { id, data, vnc_uri } = container;
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
					id: id,
					ip: IPAddress,
					uptime: !inactive ? getUptime(StartedAt) : '-',
					status: Status,
					cpu: data.cpu_percent,
					vnc_uri
				}
			})
			console.log(items)
			return items
		}
    },
    methods: { 
<<<<<<< Updated upstream
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
=======
        getInventory: function() {
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
>>>>>>> Stashed changes
				this.listContainers()
            })			
        },
		listContainers: async function() {
<<<<<<< Updated upstream
			const calls = this.inventory.map(({ slug }) => {
				return axios.get(`${this.$store.state.containerAPI}/inspect/${slug}`, {headers: this.$store.state.header})
			});
			const results = await Promise.allSettled(calls)
			const data = this.inventory.map(({ slug }, index) => {
				return {
					id: slug,
=======
			const calls = []
			this.inventory.forEach(({ slug }) => {
				calls.push(axios.get(`${this.$store.state.containerAPI}/stats/${slug}`, {headers: {...this.$store.state.header, "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate"}}));
			});
			const results = await Promise.allSettled(calls);

			const data = this.inventory.map(({ robot_id, slug, vnc_uri }, index) => {
				return {
					robot_id,
					id: slug,
					vnc_uri: `http://localhost${vnc_uri}`, // TODO: change to .env
>>>>>>> Stashed changes
					data: (results[index].status === 'fulfilled') 
						?  results[index].value.data
						:  404
				}
<<<<<<< Updated upstream
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
=======
			}).sort( (a, b) => a.robot_id > b.robot_id );
			console.log("data fetched")
			this.containerList = data
        },
		startContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/start/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
>>>>>>> Stashed changes
				this.listContainers()
            })	
		},
		stopContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/stop/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${id} stopped`)
				this.listContainers()
            })	
<<<<<<< Updated upstream
=======
		},
		removeContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/remove/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				this.listContainers()
            })
>>>>>>> Stashed changes
		}
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.getInventory()	
    },
	mounted() {
<<<<<<< Updated upstream
		//this.pollInterval = setInterval(() => this.listContainers(), 5000)
	},
	// Only hook that triggered for interval clearance (?)
	beforeRouteLeave(to, from, next) {
		//clearInterval(this.pollInterval)
		next()
	}
	
=======
		this.pollInterval = setInterval(() => this.getInventory(), 2500)
	},
	beforeDestroy() {  
        clearInterval(this.pollInterval);
    }
>>>>>>> Stashed changes
}
</script>

<style lang="scss" scoped>

</style>