import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

const domain = (process.env.NODE_ENV === "development") ? window.location.hostname : window.location.host;
const protocol = (process.env.VUE_APP_PROTOCOL === "http") ? "http" : "https";
const protocolWs = (process.env.VUE_APP_PROTOCOL === "http") ? "ws" : "wss";

const state = {
    user: null,
    baseURL: `${protocol}://` + domain + "/api/v1",
    containerAPI: `${protocol}://` + domain + "/containers",
    rootURL: `${protocol}://` + domain,
    wsRootURL: `${protocolWs}://` + domain,
    header: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
}
const getters = {
    getUser: (state) => state.user
}
const mutations = {
    SET_CURRENT_USER: (state, user) => state.user = user
}
const actions = {
    async setCurrentUser({commit}, user) {
        commit("SET_CURRENT_USER", user)
    }
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})