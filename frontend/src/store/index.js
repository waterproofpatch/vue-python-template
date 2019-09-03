import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    id: null,
    email: null
  },
  getters: {
    id: state => state.id,
    email: state => state.email
  },
  mutations: {
    setId(state, id) {
      state.id = id
    },
    setEmail(state, email) {
      state.email = email
    },
    clearAll(state) {
      state.id = null
      state.email = null
    }
  }
})

export default store