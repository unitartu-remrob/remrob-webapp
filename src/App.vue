<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <Justify v-b-toggle.sidebar-backdrop v-if="$store.state.user !== null" class="mr-2" style="cursor: pointer;" font-scale="2" variant="light" />
      <b-navbar-brand style="cursor:pointer" @click="$router.push({name:'Home'})">Remrob</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <UserSubmissionLink v-if="$store.state.user !== null"/>
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
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/inventory">Manage inventory</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/users">Users</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/admin-panel">Admin panel</b-nav-item>
            <br>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" to="/newsboard">Update newsboard</b-nav-item>
            <br>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" href="http://remrob.ut.ee/cam/" target="_blank">Camera dashboard</b-nav-item>
            <b-nav-item v-if="getUser.role == 'ROLE_ADMIN'" href="/containers/guide">Administration guide</b-nav-item>
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
    ...mapGetters(["getUser"])
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
    // getOwncloudLink: function() {
    //   this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
    //   axios.get(this.$store.state.baseURL + "/owncloud_link", {headers: this.$store.state.header}).then((res) => {
    //     this.owncloud_active = true;
    //     // this.owncloud_link =
    //     console.log(res) 
    //   }).catch(e => console.log(e))
    // }
  },
  created() {
    // this.getOwncloudLink();
    // console.log(this.getUser)
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
