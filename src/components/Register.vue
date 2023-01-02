<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%">
        <b-card>
          <b-form @submit="register">
            <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{errorMessage}}</b-alert>
            <b-alert :show="showAlert" dismissible variant="success">Registration successful</b-alert>
            <b-form-group>
              <h3 class="text-center">Register</h3>
            </b-form-group>
            <b-form-group label="First Name">
              <b-form-input required v-model="firstName"/>
            </b-form-group>
            <b-form-group label="Last Name">
              <b-form-input required v-model="lastName"/>
            </b-form-group>
            <b-form-group label="Email">
              <b-form-input required v-model="email"/>
            </b-form-group>
            <b-form-group label="Password">
              <b-form-input required v-model="password" type="password"/>
            </b-form-group>
            <b-form-group label="Confirm Password">
              <b-form-input required v-model="confirmPassword" type="password"/>
              <b-form-text v-if="password !== confirmPassword" style="color: red !important">Passwords don't match</b-form-text>
            </b-form-group>
            <b-form-group>
              <b-button type="submit" :disabled="password !== confirmPassword" block>Register</b-button>
            </b-form-group>
            <b-form-text class="text-center">Have an account?
              <router-link to="/login">Login</router-link>
            </b-form-text>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default {
  name: 'Register',
  data() {
    return {
      email: null,
      password: null,
      confirmPassword: null,
      firstName: null,
      lastName: null,
      showAlert: false,
      dismissSec: 5,
      dismissCountDown: 0,
      errorMessage: null
    }
  },
  methods: {
    register: function () {
        this.$api.post(`/api/v1/register`, {
        "email": this.email,
        "first_name": this.firstName,
        "last_name": this.lastName,
        "password": this.password,
      }).then((res) => {
        if (res.status === 200) {
          this.showAlert = true;
          setTimeout(() => this.$router.push({name: "Login"}), 2000)
        }
      }).catch((error) => {
        this.dismissCountDown = this.dismissSec
        this.errorMessage = error.response.data
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