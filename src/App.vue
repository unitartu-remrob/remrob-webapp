<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <Justify v-b-toggle.sidebar-backdrop v-if="loggedIn && isSiteAdmin" class="mr-2" style="cursor: pointer;" font-scale="2" variant="light" />
      <b-navbar-brand style="cursor:pointer" @click="homeRedirect">Remrob spot</b-navbar-brand>
      <b-navbar-nav v-if="loggedIn" class="ml-auto">
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
        v-if="loggedIn && isSiteAdmin"
        id="sidebar-backdrop"
        backdrop-variant="dark"
        backdrop
        bg-variant="dark"
        text-variant="light"     
        shadow
      >
        <nav class="mb-3">
          <b-nav vertical>
            <b-nav-item v-if="isAdmin" to="/inventory">Manage inventory</b-nav-item>
            <b-nav-item v-if="isAdmin" to="/users">Users</b-nav-item>
            <b-nav-item v-if="isAdmin" to="/admin-panel">Admin panel</b-nav-item>
          </b-nav>
        </nav>
      </b-sidebar>
    <router-view/>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { RESERVED_ADMIN_USERS } from './router/router';

export default {
  name: 'App',
  data() {
    return {
      owncloud_active: false,
      owncloud_link: null,
    }
  },
  components: {

  },
  computed: {
    ...mapGetters(["getUser"]),
    loggedIn: function() {
      return this.getUser !== null;
    },
    isAdmin: function() {
      return this.getUser.role === "ROLE_ADMIN";
    },
    isSiteAdmin: function() {
      return RESERVED_ADMIN_USERS.includes(this.getUser.user_name);
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
      if (this.isSiteAdmin) {
        this.$router.push({ name: "Home" })
      } else if (this.loggedIn) {
        this.$router.push({ name: "Session" })
      } else {
        this.$router.push({ name: "Login" })
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
