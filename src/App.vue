<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <Justify v-b-toggle.sidebar-backdrop v-if="loggedIn" class="mr-2" style="cursor: pointer;" font-scale="2" variant="light" />
      <b-navbar-brand style="cursor:pointer" @click="$router.push({ name:'Home' })">Remrob</b-navbar-brand>
      <b-navbar-nav v-if="loggedIn" class="ml-auto">
        <b-nav-item v-if="isAdmin" href="/containers/guide/" class="admin-sc mr-1">
          <b-button class="btn-dark" variant="light"><JournalText font-scale="1" class="mr-2"/>Remrob guide</b-button>
        </b-nav-item>
        <b-nav-item v-if="isAdmin" to="/newsboard" class="admin-sc mr-3">
          <b-button class="btn-dark" variant="light"><SignPost font-scale="1" class="mr-2"/>Update newsboard</b-button>
        </b-nav-item>
        <UserSubmissionLink />
        <b-nav-item>
          <b-button @click="logout">Logout</b-button>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <b-sidebar
        v-if="loggedIn"
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
            <b-nav-item v-if="isAdmin" to="/createSlot">Create slots</b-nav-item>
            <b-nav-item v-if="isAdmin" to="/inventory">Manage inventory</b-nav-item>
            <b-nav-item v-if="isAdmin" to="/users">Users</b-nav-item>
            <b-nav-item v-if="isAdmin" to="/admin-panel">Admin panel</b-nav-item>
            <br/>
            <b-nav-item v-if="isAdmin" to="/newsboard">Update newsboard</b-nav-item>
            <b-nav-item v-if="isAdmin" href="http://192.168.200.201:8000" target="_blank">Camera dashboard (only from LAN)</b-nav-item>
            <b-nav-item v-if="isAdmin" href="/containers/guide/">Administration guide</b-nav-item>
          </b-nav>
        </nav>
      </b-sidebar>
    <router-view/>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import UserSubmissionLink from './components/UserSubmissionLink.vue'

export default {
  name: 'App',
  data() {
    return {
      owncloud_active: false,
      owncloud_link: null,
    }
  },
  components: {
    UserSubmissionLink
  },
  computed: {
    ...mapGetters(["getUser"]),
    loggedIn: function() {
      return this.getUser !== null;
    },
    isAdmin: function() {
      return this.getUser.role === "ROLE_ADMIN";
    }
  },

  methods: {
    ...mapActions(["setCurrentUser"]),

    logout: function() {
      this.$api.delete("/api/v1/logout").then((res) => {
        this.setCurrentUser(null)
        localStorage.removeItem("user");
        this.$router.push({name: "Login"})
      })
    },
  },
  created() {

  }
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
