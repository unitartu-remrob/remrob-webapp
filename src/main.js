import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
import router from './router/router'
import store from './store/store'
import authentication from './plugins/authentication'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(authentication)

Vue.$keycloak.init({ onload: 'login-required' }).then(() => {
  new Vue({
    router,
    store,
    render: h => h(App),
  }).$mount('#app')
})


