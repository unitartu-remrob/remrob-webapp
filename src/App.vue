<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <Justify v-b-toggle.sidebar-backdrop v-if="loggedIn && isAdmin" class="mr-2" style="cursor: pointer;" font-scale="2" variant="light" />
      <b-navbar-brand style="cursor:pointer" @click="homeRedirect" class="remrob-site-brand">Remrob</b-navbar-brand>
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
      <b-navbar-nav v-else-if="$route.path !== '/login'" class="ml-auto">
        <b-nav-item class="mr-3">
          <b-button @click="$router.push({ name: 'Login' })">Login</b-button>
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
        this.$router.push({ name: "Login" })
      })
    },

    homeRedirect: function() {
      if (this.loggedIn) {
        this.$router.push({ name: "Home" })
      } else {
        this.$router.push({ name: "Landing" })
      }
    }
  },
  created() {

  }
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Arvo:ital,wght@0,400;0,700;1,400;1,700&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');

  #app {
    overflow-x: hidden;
  }

  .b-sidebar .nav-item > a {
    color: white !important;
  }


  .b-sidebar .nav-item > a:hover {
    color: gray !important;
  }

  .remrob-site-brand {
    font-size: 1.4rem !important;
  }
</style>
