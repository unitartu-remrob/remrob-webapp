<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card>
          <b-form>
            <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">Login failed</b-alert>
            <b-form-group>
              <h3 class="text-center">Login</h3>
            </b-form-group>
            <b-form-group label="E-mail">
              <b-form-input v-model="email" />
            </b-form-group>
            <b-form-group label="Password">
              <b-form-input v-model="password" type="password" />
            </b-form-group>
            <b-form-group>
              <b-button block @click="login">Login</b-button>
            </b-form-group>
            <b-form-text class="text-center">No account? <router-link to="/register">Register</router-link></b-form-text>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      email: null,
      password: null,
      showAlert: false,
      dismissSec: 5,
      dismissCountDown: 0
    }
  },
  methods: {
    ...mapActions(["setCurrentUser"]),

    login: function() {
      axios.post(this.$store.state.baseURL + "/login", {
        "email": this.email,
        "password": this.password,
      }).then((res) => {
          console.log(res)
        this.setCurrentUser(res.data)
        this.$router.push({name:"Home"})
      }).catch((error) => {
        this.dismissCountDown = this.dismissSec
      })
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    }

  },
}
</script>

<style scoped>

</style>