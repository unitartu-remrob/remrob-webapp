<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card>
          <b-form>
            <b-alert :show="dismissCountDown" dismissible :variant="alertType" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{message}}</b-alert>
            <b-form-group class="text-center">
              <h3>Forgot Password</h3>
            </b-form-group>
            <b-form-group label="E-mail:">
              <b-form-input @keyup.enter="resetRequest" v-model="email" />
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

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: null,
      showAlert: false,
      message: null,
      alertType: "info",
      dismissSec: 5,
      dismissCountDown: 0
    }
  },
  methods: {
    resetRequest: function() {
        const data = { "email": this.email };
        this.email = "";
        this.$api.post(`/api/v1/password_reset`, data).then((res) => {
          if (res.data === "Email sent") {
            this.alertType = "success"
            this.message = res.data
            this.dismissCountDown = this.dismissSec
          }
        }).catch(error => {
          this.alertType = "danger"
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