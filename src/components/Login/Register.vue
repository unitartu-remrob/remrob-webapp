<template>
  <div class="login-container">
    <b-row align-h="end">
      <b-col style="max-width: 35rem; margin: 5% 17.5%;">
        <b-card class="login-box">
          <b-form @submit="register" class="register-form p-1">
            <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{errorMessage}}</b-alert>
            <b-alert :show="showAlert" dismissible variant="success">Register successful. Check your email for confirmation.</b-alert>
            <b-form-group>
              <h3 class="text-center">Register</h3>
            </b-form-group>
            <b-row class="timepicker-row mb-3">
              <b-col cols="6">
                  <label class="timepicker-label">First name</label>
                  <b-form-input required v-model="firstName"/>
              </b-col>
              <b-col cols="6">
                  <label class="timepicker-label">Last name</label>
                  <b-form-input required v-model="lastName"/>
              </b-col>
            </b-row>
            <b-form-group label="Email">
              <b-form-input required v-model="email"/>
            </b-form-group>
            <!-- <b-form-group label="Occupation (optional)">
              <b-form-input required v-model="email"/>
            </b-form-group> -->
            <b-form-group label="Password">
              <b-form-input required v-model="password" type="password"/>
            </b-form-group>
            <b-form-group label="Confirm Password">
              <b-form-input required v-model="confirmPassword" type="password"/>
              <b-form-text v-if="password !== confirmPassword" style="color: red !important">Passwords don't match</b-form-text>
            </b-form-group>
            <b-form-group>
              <b-button type="submit" :disabled="password !== confirmPassword" block class="mt-2">Register</b-button>
            </b-form-group>
            <b-form-text class="text-center">Have an account?
              <router-link to="/login">Login</router-link>
            </b-form-text>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
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
      occupation: null,
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

.login-box {
  padding: 0.2rem 1rem;
}
</style>