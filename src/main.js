import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue';
import wysiwyg from "vue-wysiwyg";

import {
  BIconJustify,
  BIconCircleFill,
  BIconPersonFill,
  BIconExclamationLg,
  BIconTv,
  BIconBroadcast,
  BIconLink45deg,
  BIconClock,
  BIconSignpost,
  BIconCodeSquare,
  BIconFilm,
  BIconJournalText,
  BIconBox,
  BIconArrowRight,
  BIconEject
} from 'bootstrap-vue'
import router from './router/router'
import store from './store/store'
import { api } from './util/api'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(wysiwyg, {})
Vue.component('Justify', BIconJustify)
Vue.component('CircleFill', BIconCircleFill)
Vue.component('PersonFill', BIconPersonFill)
Vue.component('Exclamation', BIconExclamationLg)
Vue.component('Screen', BIconTv)
Vue.component('Broadcast', BIconBroadcast)
Vue.component('Link', BIconLink45deg)
Vue.component('Clock', BIconClock)
Vue.component('SignPost', BIconSignpost)  //journal-code
Vue.component('JournalCode', BIconCodeSquare)
Vue.component('JournalText', BIconJournalText)
Vue.component('FilmIcon', BIconFilm)
Vue.component('Box', BIconBox)
Vue.component('Eject', BIconEject)
Vue.component('ArrowRight', BIconArrowRight)

Vue.prototype.$api = api;

window.eventBus = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')



