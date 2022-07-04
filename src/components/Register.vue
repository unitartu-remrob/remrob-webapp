<template>
  <b-container>
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%">
        <b-card>
          <b-form>
            <b-form-group>
              <h3 class="text-center">Register</h3>
            </b-form-group>
            <b-form-group label="Email">
              <b-form-input v-model="email"/>
            </b-form-group>
            <b-form-group label="Password">
              <b-form-input v-model="password" type="password"/>
            </b-form-group>
            <b-form-group>
              <b-button block @click="register">Register</b-button>
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
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      email: null,
      password: null,
    }
  },
  methods: {
    register: function () {
      axios.post(this.$store.state.baseURL + "/register", {
        "email": this.email,
        "password": this.password,
      }).then((res) => {
        if (res.status == 200) {
          this.$router.push({name: "Login"})
        }
      })
    }
  },
}
</script>

<style scoped>

</style>