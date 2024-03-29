import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue';

// import ErrorPage from 'vue-error-page';

import {
  BIconJustify,
  BIconCircleFill,
  BIconPersonFill,
  BIconExclamationLg,
  BIconTv,
  BIconBroadcast,
  BIconLink45deg,
  BIconClock
} from 'bootstrap-vue'
import router from './router/router'
import store from './store/store'
import { api } from './util/api'
// import authentication from './plugins/authentication'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.config.productionTip = false

// Vue.use(ErrorPage);

Vue.use(BootstrapVue)
Vue.component('Justify', BIconJustify)
Vue.component('CircleFill', BIconCircleFill)
Vue.component('PersonFill', BIconPersonFill)
Vue.component('Exclamation', BIconExclamationLg)
Vue.component('Screen', BIconTv)
Vue.component('Broadcast', BIconBroadcast)
Vue.component('Link', BIconLink45deg)
Vue.component('Clock', BIconClock)

Vue.prototype.$api = api;

window.eventBus = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')



