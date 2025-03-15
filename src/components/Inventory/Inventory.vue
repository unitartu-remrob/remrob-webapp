<template>
    <b-container fluid class="pt-3 pl-4 bg-white">
        <b-alert :show="dismissCountDown" dismissible @dismissed="dismissCountDown=0" :variant="alertType">{{message}}</b-alert>
        <b-modal ok-title="Confirm" @ok="deleteInventory(selectedForDelete)" title="Delete inventory item" id="delete-modal">
            <h4>Are you sure you want to remove this inventory item?</h4>
        </b-modal>
        <b-row class="mt-3">
            <b-col class="col-4">
                <b-form>
                    <b-form-group label="Robot nr.:">
                        <b-form-input type="number" v-model="robotId">  
                        </b-form-input>
                    </b-form-group>
                    <b-form-group label="Robot name:">
                        <b-form-input type="text" v-model="robotLabel">  
                        </b-form-input>
                    </b-form-group>
                    <b-button variant="success" @click="createInventory">Add robot</b-button>
                </b-form>
            </b-col>
            <b-col class="col-6">
                <h1 class="text-center panel-title">Inventory</h1>
            </b-col>
        </b-row>
        <br>
        <b-row>
            <b-col class="col-8">
                <h2>Robots</h2>
            </b-col>
            <b-col>
                <h2>Simtainers</h2>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-table striped :items="inventory" :fields="fields">
                    <template #cell(delete)="{ item: { slug } }">
                        <b-button type="button" class="delete-button" variant="dark" @click="function() {selectedForDelete = slug; $bvModal.show('delete-modal')}">Remove</b-button>
                    </template>
                    <template #cell(project)="{ item }">
                        <InventoryInput :inventoryItem="item" :isSimtainer=false @update="updateInventory"/>
                    </template>
                </b-table>
            </b-col>
            <b-col class="col-4 ml-5">
                
                <b-table :items="simtainerInventory" :fields="simtainerFields">
                    <template #cell(open_to_public)="{ item }">
                        <InventoryInput :inventoryItem="item" :isSimtainer=true @update="updateSimtainerInventory"/>
                    </template>    
                </b-table>
            </b-col>
        </b-row>
        <b-row>
            <b-col class="d-flex justify-content-center align-items-center">
                <b-img style="max-width: 20vw" :src="require('@/assets/field_plan.jpg')"></b-img>
                <h4>⬅️ Cell legend relative to door</h4>
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
            robotLabel: null,
            inventory: [],
            simtainerInventory: [],
            formState: [],
            fields: [
                { key: "robot_id", label: "ID" },
                { key: "robot_label", label: "Robot name" },
                // { key: "location", label: "Workcell" },
                { key: "project", label: "Change settings" },              
                // { key: "status", label: "Available" },
                { key: "delete", label: ""},
            ],
            simtainerFields: [
                { key: "slug", label: "ID" },         
                { key: "open_to_public", label: "Public access" },
            ],
            selectedForDelete: null,
            message: "",
            dismissSec: 3,
            dismissCountDown: 0,
            alertType: "",
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
            this.getRobotInventory()
            this.getSimtainerInventory()
        },
        getRobotInventory: function() {
            this.$api.get(`/api/v1/inventory`).then((res) => {
                this.inventory = res.data
            })
        },
        getSimtainerInventory: function() {
            this.$api.get(`/api/v1/simtainers`).then((res) => {
                this.simtainerInventory = res.data
            })
        },
        createInventory: function() {
            if (this.robotId === null) {
                return 
            }
            const data = {
                "robot_id": this.robotId,
                "robot_label": this.robotLabel
            }
            this.$api.post(`/api/v1/inventory`, data).then((res) => {
                this.robotId = null;
                this.robotLabel = null;
                
                this.message = res.data;
                this.alertType = "success";
                this.dismissCountDown = this.dismissSec;
                this.getRobotInventory()
            })
        },
        deleteInventory: function(id) {
            this.inventory = this.inventory.filter(item => item.slug !== id)
            this.$api.delete(`/api/v1/inventory/${id}`).then((res) => {
                this.message = res.data;
                this.alertType = "info";
                this.dismissCountDown = this.dismissSec;
            })
        },
        updateInventory: function(item) {
			const data = {
				"project": item.project,
                "cell": item.cell,
                "status": item.status
			}
            this.$api.put(`/api/v1/inventory/${item.slug}`, data).then((res) => {
				this.message = res.data;
                this.alertType = "success";
                this.dismissCountDown = this.dismissSec;
			})
		},
        updateSimtainerInventory: function(item) {
            const data = {
                "open_to_public": item.open_to_public
            }
            this.$api.put(`/api/v1/simtainers/${item.slug}`, data).then((res) => {
                this.message = res.data;
                this.alertType = "success";
                this.dismissCountDown = this.dismissSec;
            })
        }
    },
    created() {
        this.getInventory()
    }
}
</script>

<style lang="css" scoped>

.panel-title {
    font-size: 2.8rem;
}
</style>