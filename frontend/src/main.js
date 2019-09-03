import Vue from 'vue'
import App from './App.vue'
import Register from './components/Register.vue'
import Login from './components/Login.vue'

Vue.config.productionTip = false

// axios
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
// done axios

// vue router
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
    path: '/register',
    component: Register
  },
  {
    path: '/login',
    component: Login
  },
]

const router = new VueRouter({
  routes // short for `routes: routes`
})
// done vue router

new Vue({
  render: h => h(App),
  router
}).$mount('#app')