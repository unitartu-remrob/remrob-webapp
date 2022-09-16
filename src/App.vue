<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <Justify v-b-toggle.sidebar-backdrop v-if="$store.state.user !== null" class="mr-2" style="cursor: pointer;" font-scale="2" variant="light" />
      <b-navbar-brand style="cursor:pointer" @click="$router.push({name:'Home'})">Remrob</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item>
          <b-button v-if="$store.state.user !== null" @click="logout">Logout</b-button>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <b-sidebar
        v-if="$store.state.user !== null"
        id="sidebar-backdrop"
        backdrop-variant="dark"
        backdrop
        bg-variant="dark"
        text-variant="light"
        shadow
      >
        <nav class="mb-3">
          <b-nav vertical>
            <b-nav-item to="/booking">Booking</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/createSlot">Create slots</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/inventory">Create inventory</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/users">Users</b-nav-item>
            <b-nav-item to="/user-panel">User panel</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/admin-panel">Admin panel</b-nav-item>
          </b-nav>
        </nav>
      </b-sidebar>
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
      axios.delete(this.$store.state.baseURL + "/logout", {headers: this.$store.state.header}).then((res) => {
        this.setCurrentUser(null)
        this.$router.push({name: "Login"})
      })
    }
  },
}
</script>

<style>
  #app {
    overflow-x: hidden;
  }

  .b-sidebar .nav-item > a {
    color: white !important;
  }


  .b-sidebar .nav-item > a:hover {
    color: gray !important;
  }

 
</style>
