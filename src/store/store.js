import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

const state = {
    /** @type {?User} */
    user: JSON.parse(localStorage.getItem('user')),
}
const getters = {
    /**
     * Returns current user data
     * @typedef {Object} User
     * @property {number} user_id
     * @property {string} role
     * @property {string} access_token
     * @returns {User}
     */
    getUser: (state) => state.user
}
const mutations = {
    SET_CURRENT_USER: (state, user) => {
        localStorage.setItem("user", JSON.stringify(user));
        return state.user = user;
    },
}
const actions = {
    async setCurrentUser({commit}, user) {
        commit("SET_CURRENT_USER", user)
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})

export default store;