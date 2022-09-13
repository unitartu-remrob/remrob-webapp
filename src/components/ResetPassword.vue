<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card>
          <b-form>
            <b-form-group>
              <h3 class="text-center">Reset password</h3>
            </b-form-group>
            <b-form-group label="Password">
              <b-form-input v-model="password" type="password" />
            </b-form-group>
            <b-form-group>
              <b-button :disabled="!password" block @click="resetPassword">Submit</b-button>
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
  name: 'ResetPassword',
  data() {
    return {
      password: null,
    }
  },
  methods: {
    resetPassword: function() {
        axios.post(this.$store.state.baseURL + "/password_reset_verified/" + this.$route.params.token, {"password": this.password}).then((res) => {
            if (res.data === "Password changed") {
              this.$router.push({name: "Login"})
            }
        })
    }
  },
}
</script>

<style scoped>

</style>