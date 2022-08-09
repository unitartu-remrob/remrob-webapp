<template>
    <b-container fluid>
        <b-row>
            <b-col>
                <b-form>
                    <b-form-group label="Robot ID">
                        <b-form-input type="number" v-model="robotId">  
                        </b-form-input>
                    </b-form-group>
                    <b-button @click="createInventory">Submit</b-button>
                </b-form>
            </b-col>
        </b-row>
        <br>
        <b-row>
            <b-col>
                <b-table striped :items="inventory" :fields="fields">
                    <template #cell(delete)="{ item: { slug } }">
                        <b-button type="button" class="delete-button" variant="dark" @click="deleteInventory(slug)">Remove</b-button>
                    </template>
                    <template #cell(project)="{ item }">
                        <InventoryInput :inventoryItem="item" @update="updateInventory"/>
                    </template>
                </b-table>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import InventoryInput from './InputForm.vue'
export default {
    data() {
        return {
            robotId: null,
            inventory: [],
            formState: [],
            fields: [
                { key: "title", label: "Name" },
                { key: "project", label: "Location" },
                // { key: "status", label: "Available" },
                { key: "delete", label: ""}
            ]
        }
    },
    components: {
        InventoryInput
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        getInventory: function() {
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
            })
        },
        createInventory: function() {
            if (this.robotId === null) {
                console.log("empty submit")
                return 
            }
            const data = {
                "robot_id": this.robotId
            }
            axios.post(this.$store.state.baseURL + "/inventory", data, {headers: this.$store.state.header}).then((res) => {
                this.robotId = null;
                this.getInventory()
            })
        },
        deleteInventory: function(id) {
            this.inventory = this.inventory.filter(item => item.slug !== id)

            axios.delete(this.$store.state.baseURL + `/inventory/${id}`, {headers: this.$store.state.header}).then((res) => {
                console.log("Item deleted")
            })
        },
        updateInventory: function(item) {
			const data = {
				"project": item.project
			}
			axios.put(this.$store.state.baseURL + `/inventory/${item.slug}`, data, {headers: this.$store.state.header}).then((res) => {
				
			})
		}
    },
    created() {
        this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
        this.getInventory()
    }
}
</script>

<style lang="scss" scoped>

</style>