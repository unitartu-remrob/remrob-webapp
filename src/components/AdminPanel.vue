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
        getInventory: function() {
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
				this.listContainers()
            })			
        },
		listContainers: async function() {
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
					data: (results[index].status === 'fulfilled') 
						?  results[index].value.data
						:  404
				}
			}).sort( (a, b) => a.robot_id > b.robot_id );
			console.log("data fetched")
			this.containerList = data
        },
		startContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/start/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				this.listContainers()
            })	
		},
		stopContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/stop/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				console.log(`${id} stopped`)
				this.listContainers()
            })	
		},
		removeContainer: function(id) {
			axios.post(`${this.$store.state.containerAPI}/remove/${id}`, {}, {headers: this.$store.state.header}).then((res) => {
				this.listContainers()
            })
		}
    },
    created() {
		this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.getInventory()	
    },
	mounted() {
		this.pollInterval = setInterval(() => this.getInventory(), 2500)
	},
	beforeDestroy() {  
        clearInterval(this.pollInterval);
    }
}
</script>

<style lang="scss" scoped>

</style>