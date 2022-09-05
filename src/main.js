import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue';
// import ErrorPage from 'vue-error-page';

import {
  BIconCircleFill,
  BIconPersonFill,
  BIconExclamationLg,
  BIconTv
} from 'bootstrap-vue'
import router from './router/router'
import store from './store/store'
// import authentication from './plugins/authentication'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

// Vue.use(ErrorPage);

Vue.use(BootstrapVue)
Vue.component('CircleFill', BIconCircleFill)
Vue.component('PersonFill', BIconPersonFill)
Vue.component('Exclamation', BIconExclamationLg)
Vue.component('Screen', BIconTv)

window.eventBus = new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')



