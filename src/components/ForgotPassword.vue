<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card>
          <b-form>
            <b-alert :show="dismissCountDown" dismissible variant="success" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">Email sent</b-alert>
            <b-form-group>
              <h3 class="text-center">Forgot Password</h3>
            </b-form-group>
            <b-form-group label="E-mail">
              <b-form-input v-model="email" />
            </b-form-group>
            <b-form-group>
              <b-button :disabled="!email" block @click="resetRequest">Submit</b-button>
            </b-form-group>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: null,
      showAlert: false,
      dismissSec: 5,
      dismissCountDown: 0
    }
  },
  methods: {
    resetRequest: function() {
        axios.post(this.$store.state.baseURL + "/password_reset", {"email": this.email}).then((res) => {
            if (res.data === "Email sent") {
              this.dismissCountDown = this.dismissSec
            }
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