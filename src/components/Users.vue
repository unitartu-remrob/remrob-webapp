<template>
    <b-container fluid>
        <b-table striped :items="users"></b-table>

    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
export default {
    data() {
        return {
            users: null
        }
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        getUsers: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/users", {headers: this.$store.state.header}).then((res) => {
                this.users = res.data
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