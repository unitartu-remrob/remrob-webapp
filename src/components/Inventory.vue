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
        <b-row>
            <b-col class="d-flex justify-content-center mt-2">
                <b-img style="max-width: 20vw" :src="require('../assets/field_plan.jpg')"></b-img>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import InventoryInput from './InputForm.vue'
export default {
    data() {
        return {
            robotId: null,
            inventory: [],
            formState: [],
            fields: [
                { key: "title", label: "" },
                // { key: "location", label: "Workcell" },
                { key: "project", label: "" },              
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
            this.$api.get(`/api/v1/inventory`).then((res) => {
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
            this.$api.post(`/api/v1/inventory`, data).then((res) => {
                this.robotId = null;
                this.getInventory()
            })
        },
        deleteInventory: function(id) {
            this.inventory = this.inventory.filter(item => item.slug !== id)
            this.$api.delete(`/api/v1/inventory/${id}`).then((res) => {
                console.log("Item deleted")
            })
        },
        updateInventory: function(item) {
			const data = {
				"project": item.project,
                "cell": item.cell
			}
            this.$api.put(`/api/v1/inventory/${item.slug}`, data).then((res) => {
				
			})
		}
    },
    created() {
        this.getInventory()
    }
}
</script>

<style lang="scss" scoped>

</style>