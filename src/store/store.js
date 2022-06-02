import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

const state = {
    currentUserId: null,
    baseURL: "http://" + window.location.hostname + ":5000/api/v1" 
}
const getters = {
    getCurrentUserId: (state) => state.currentUserId
}
const mutations = {
    SET_CURRENT_USER_ID: (state, currentUserId) => state.currentUserId = currentUserId
}
const actions = {
    async setCurrentUserId({commit}, currentUserId) {
        commit("SET_CURRENT_USER_ID", currentUserId)
    }
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})