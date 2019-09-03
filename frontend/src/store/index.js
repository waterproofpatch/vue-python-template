import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    uid: null,
    email: null,
    test: "test value"
  },
  getters: {
    uid: state => state.uid,
    email: state => state.email,
    test: state => state.test
  },
  mutations: {
    login(state, uid, email) {
      state.uid = uid;
      state.email = email;
    },
    logout(state) {
      state.uid = null
      state.email = null
    }
  }
})

export default store