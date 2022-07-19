<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <b-navbar-brand style="cursor:pointer" @click="$router.push({name:'Home'})">Remrob</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item>
          <b-button v-if="$store.state.user !== null" @click="logout">Logout</b-button>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions, mapGetters } from 'vuex';
export default {
  name: 'App',
  components: {
  },
  computed: {
    ...mapGetters(["getUser"])
  },

  methods: {
    ...mapActions(["setCurrentUser"]),

    logout: function() {
      this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
      axios.delete(this.$store.state.baseURL + "/logout", {headers: this.$store.state.header}).then((res) => {
        this.setCurrentUser(null)
        this.$router.push({name: "Login"})
      })
    }
  },
}
</script>

<style>

</style>
