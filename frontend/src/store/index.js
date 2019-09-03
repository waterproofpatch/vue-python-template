import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    uid: null,
    email: null
  },
  getters: {
    uid: state => state.uid,
    email: state => state.email
  },
  mutations: {
    setUid(state, uid) {
      state.uid = uid
    },
    setEmail(state, email) {
      state.email = email
    },
    clearAll(state) {
      state.uid = null
      state.email = null
    }
  }
})

export default store