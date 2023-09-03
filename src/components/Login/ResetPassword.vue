<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card>
          <b-alert :show="dismissCountDown" dismissible variant="info" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{message}}</b-alert>
          <b-form v-if="!reset">
            <b-form-group>
              <h3 class="text-center">Reset password</h3>
            </b-form-group>
            <b-form-group label="Enter new password:">
              <b-form-input v-model="password" @keyup.enter="resetPassword" type="password" />
            </b-form-group>
            <b-form-group>
              <b-button :disabled="!password" block @click="resetPassword">Submit</b-button>
            </b-form-group>
          </b-form>
          <div v-else>
            <b-form-group>
              <h3 class="text-center">Password reset</h3>
            </b-form-group>
            <b-form-group>
              <p class="text-center">Your password has been reset.</p>
            </b-form-group>
            <b-form-group>
              <b-button block @click="$router.push({ name: 'Login' })">Login</b-button>
            </b-form-group>
          </div>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default {
  name: 'ResetPassword',
  data() {
    return {
      password: null,
      reset: false,
      message: null,
      dismissSec: 5,
      dismissCountDown: 0
    }
  },
  methods: {
    resetPassword: function() {
        const data = { "password": this.password } // save password in data object
        this.$api.post(`/api/v1/password_reset_verified/${this.$route.params.token}`, data).then((res) => {
            if (res.data === "Password changed") {
              // this.$router.push({name: "Login"})
              this.reset = true;
            } else {
              this.message = "Password reset failed due to server error. Try again later."
              this.dismissCountDown = this.dismissSec
            }
        }).catch(error => {
          this.message = error.response.data
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