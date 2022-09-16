<template>
    <b-container fluid>
        <b-row>
            <b-col>
                <b-table striped :items="users" :fields="fields">
                    <template #cell(role)="data">
                        <b-form-input v-model="users[data.index].role"></b-form-input>
                    </template>
                    <template #cell(active)="data">
                        <b-form-checkbox switch v-model="users[data.index].active"></b-form-checkbox>
                    </template>
                </b-table>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-button @click="updateUsers">Save</b-button>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
axios.defaults.withCredentials = true


export default {
    data() {
        return {
            users: null,
            fields: [
                { key: "id", label: "User ID" },
                { key: "email", label: "Email" },
                { key: "role", label: "Role" },
                { key: "active", label: "Active" },
            ],
        }
    },
    computed: {
        ...mapGetters(["getUser"]),
    },
    methods: {
        getUsers: function() {
            
            axios.get(this.$store.state.baseURL + "/users", {headers: this.$store.state.header}).then((res) => {
                this.users = res.data
            })
        },
        updateUsers: function() {
            
            axios.put(this.$store.state.baseURL + "/users", this.users ,{headers: this.$store.state.header}).then((res) => {
                this.getUsers();
            })
        }
    },

    created() {
        this.getUsers()
    }
    
}
</script>

<style>

</style>