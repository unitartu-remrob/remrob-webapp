import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

const state = {
    user: null,
    baseURL: "http://" + window.location.hostname + "/api/v1",
    containerAPI: "http://" + window.location.hostname + "/containers",
    header: {
        'Authorization': '',
        'Content-Type': 'application/json',
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