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
export default {
    data() {
        return {
            users: null,
            fields: [
                { key: "id", label: "User ID" },
                { key: "first_name", label: "First Name" },
                { key: "last_name", label: "Last Name" },
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
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/users", {headers: this.$store.state.header}).then((res) => {
                this.users = res.data
            })
        },
        updateUsers: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
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