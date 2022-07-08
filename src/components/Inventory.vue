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
                <b-table striped :items="inventory"></b-table>
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
            inventory: []
        }
    },   
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        getInventory: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                this.inventory = res.data
            })
        },
        createInventory: function() {
            var data = {
                "container_id": this.containerId,
                "robot_id": this.robotId
            }
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.post(this.$store.state.baseURL + "/inventory", data, {headers: this.$store.state.header}).then((res) => {
                this.robotId = null;
                this.containerId = null;
                this.getInventory()
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