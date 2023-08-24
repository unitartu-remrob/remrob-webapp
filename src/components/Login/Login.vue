<template>
  <div class="login-container">
    <b-row align-h="center">
      <b-col style="max-width: 35rem; margin-top: 10%;">
        <b-card class="login-box">
          <b-alert :show="dismissCountDown" dismissible :variant="alertType" @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">{{errorMessage}}</b-alert>
          <b-form class="login-form">
            <b-form-group>
              <h3 class="text-center">Login</h3>
            </b-form-group>
            <b-form-group label="E-mail">
              <b-form-input @keyup.enter="login" v-model="email" />
            </b-form-group>
            <b-form-group label="Password">
              <b-form-input @keyup.enter="login" v-model="password" type="password" />
            </b-form-group>
            <b-form-group>
              <b-button block @click="login" class="mt-2">Login</b-button>
            </b-form-group>
            <b-form-text class="text-center">No account? <router-link to="/register">Register</router-link></b-form-text>
            <b-form-text class="text-center">Forgot password? <router-link to="/forgot">Reset</router-link></b-form-text>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      email: null,
      password: null,
      alertType: "",
      showAlert: false,
      dismissSec: 5,
      dismissCountDown: 0,
      errorMessage: null
    }
  },
  methods: {
    ...mapActions(["setCurrentUser"]),

    login: function() {
      this.$api.post("/api/v1/login", {
        "email": this.email,
        "password": this.password,
      }).then((res) => {
        console.log(res)
        if (res.data.access_token) {
          localStorage.setItem("user", JSON.stringify(res.data));
          this.$api.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access_token;
        }
        this.setCurrentUser(res.data)
        this.$router.push({name:"Home"})
      }).catch((error) => {
        if (error.response.status === 400) {
          this.alertType = "danger"
        } else {
          this.alertType = "info"
        }
        this.errorMessage = error.response.data
        this.dismissCountDown = this.dismissSec
      })
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    }

  },
}
</script>

<style>
.login-container {
  background-image: url('../../assets/login_bg.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  height: 94.35vh;
}

.login-box {
  box-shadow: 9px 13px 52px 13px rgba(0,0,0,0.18);
  border-radius: 15px !important;
}

.login-form {
  padding: 0.2rem 0.7rem;
}

@media (max-width: 768px) {
  /* Remove background image on mobile */
  .login-container {
    background-image: none;
  }
  .login-box {
    box-shadow: none;
  }
  .login-form {
    padding: 0;
  }
}

</style>