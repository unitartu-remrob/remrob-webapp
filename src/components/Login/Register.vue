<template>
  <div class="login-container">
    <b-row align-h="end">
      <b-col style="max-width: 35rem; margin: 5% 17.5%;">
        <b-card class="login-box">
          <b-form @submit="register" class="register-form p-1">
            <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{errorMessage}}</b-alert>
            <b-alert :show="showAlert" dismissible variant="success">Robot {{this.email}} successfully registered.</b-alert>
            <b-form-group>
              <h3 class="text-center">Register robot user</h3>
            </b-form-group>
            <b-form-group label="Robot ID (format: `$name-$id`), e.g. robotont-3">
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
    register: function (event) {
        event.preventDefault();
        this.$api.post(`/api/v1/register`, {
        "email": this.email,
        "first_name": "",
        "last_name": "",
        "password": this.password,
      }).then((res) => {
        if (res.status === 200) {
          this.showAlert = true;
          setTimeout(() => this.dismissAlert(), 3000)
        }
      }).catch((error) => {
        if (error.response.status === 500) {
          this.errorMessage = "Something went wrong."
        } else {
          this.errorMessage = error.response.data
        }
        this.dismissCountDown = this.dismissSec
      })
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    dismissAlert() {
      this.showAlert = false;
      this.email = null;
      this.password = null;
      this.confirmPassword = null;
    }
  },
}
</script>

<style scoped>

.login-box {
  padding: 0.2rem 1rem;
}
</style>