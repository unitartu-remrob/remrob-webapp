import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
import { BIconCircleFill, BIconPersonFill, BIconExclamationLg } from 'bootstrap-vue'
import router from './router/router'
import store from './store/store'
// import authentication from './plugins/authentication'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.component('CircleFill', BIconCircleFill)
Vue.component('PersonFill', BIconPersonFill)
Vue.component('Exclamation', BIconExclamationLg)
// Vue.use(authentication)

// Vue.$keycloak.init({ onload: 'login-required' }).then(() => {
//   new Vue({
//     router,
//     store,
//     render: h => h(App),
//   }).$mount('#app')
// })
new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')



