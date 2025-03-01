<template>
    <b-container fluid class="pt-3 bg-white">
        <b-alert :show="dismissCountDown" dismissible @dismissed="dismissCountDown=0" :variant="alertType">{{message}}</b-alert>
        <b-modal ok-title="Confirm" @ok="deleteInventory(selectedForDelete)" title="Delete user" id="delete-modal">
            <h4>Are you sure you want to remove this inventory item?</h4>
        </b-modal>
        <b-row class="mt-3">
            <b-col>
                <b-form>
                    <b-form-group label="Robot nr.">
                        <b-form-input type="number" v-model="robotId">  
                        </b-form-input>
                    </b-form-group>
                    <b-form-group label="Robot name">
                        <b-form-input type="string" v-model="robotLabel">  
                        </b-form-input>
                    </b-form-group>
                    <b-button @click="createInventory">Submit</b-button>
                </b-form>
            </b-col>
            <b-col>
                <h1 class="text-center panel-title">Robot inventory</h1>
            </b-col>
        </b-row>
        <br>
        <b-row>
            <b-col>
                <b-table striped :items="inventory" :fields="fields">
                    <template #cell(delete)="{ item: { slug } }">
                        <b-button type="button" class="delete-button" variant="dark" @click="function() {selectedForDelete = slug; $bvModal.show('delete-modal')}">Remove</b-button>
                    </template>
                    <template #cell(project)="{ item }">
                        <InventoryInput :inventoryItem="item" @update="updateInventory"/>
                    </template>            
                </b-table>
            </b-col>
        </b-row>
        <b-row>
            <b-col class="d-flex justify-content-center mt-3 align-items-center">
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
            formState: [],
            fields: [
                { key: "title", label: "ID" },
                { key: "robot_label", label: "Robot name" },
                // { key: "location", label: "Workcell" },
                { key: "project", label: "Change settings" },              
                // { key: "status", label: "Available" },
                { key: "delete", label: ""},
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
            this.$api.get(`/api/v1/inventory`).then((res) => {
                this.inventory = res.data
                console.log(this.inventory)
            })
        },
        createInventory: function() {
            if (this.robotId === null) {
                console.log("empty submit")
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
                this.getInventory()
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