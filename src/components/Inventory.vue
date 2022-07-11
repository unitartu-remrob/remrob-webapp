<template>
    <b-container fluid>
        <b-row>
            <b-col>
                <b-form>
                    <b-form-group label="Robot ID">
                        <b-form-input type="number" v-model="robotId">  
                        </b-form-input>
                    </b-form-group>
                    <b-form-group label="Container ID">
                        <b-form-input type="number" v-model="containerId"></b-form-input>
                    </b-form-group>
                    <b-button @click="createInventory">Submit</b-button>
                </b-form>
            </b-col>
        </b-row>
        <br>
        <b-row>
            <b-col>
                <b-table striped :items="inventory" :fields="fields">
                    <template v-for="(field, index) in fields" #[`cell(${field.key})`]="data">
                        <div :key="index" :value="inventory[data.index][field.key]">
                            {{inventory[data.index][field.key]}}
                            <b-button v-if="field.key === 'delete'" type="button" class="delete-button" variant="dark" @click="deleteInventory(data.index)">Delete</b-button>
                        </div>                     
                    </template>
                </b-table>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
export default {
    data() {
        return {
            robotId: null,
            containerId: null,
            inventory: [],
            fields: [
                { key: "robot_id", label: "Robot ID" },
                { key: "server_container_id", label: "Container ID" },
                { key: "title", label: "Name" },
                { key: "delete", label: ""}
            ]
        }
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
            var data = {
                "container_id": this.containerId,
                "robot_id": this.robotId
            }
            axios.post(this.$store.state.baseURL + "/inventory", data, {headers: this.$store.state.header}).then((res) => {
                this.robotId = null;
                this.containerId = null;
                this.getInventory()
            })
        },
        deleteInventory: function(index) {
            const pk_ID = this.inventory[index]["id"];
            this.inventory = this.inventory.filter((item, i) => i !== index)   

            axios.delete(this.$store.state.baseURL + `/inventory/${pk_ID}`, {headers: this.$store.state.header}).then((res) => {
                console.log("Item deleted")
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