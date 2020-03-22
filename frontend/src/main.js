import Vue from "vue";
import App from "./App.vue";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import Index from "./components/Index.vue";
import Items from "./components/Items.vue";

import store from "./store";

Vue.config.productionTip = false;

// axios
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
// end axios

// vue router
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/register",
    component: Register,
    name: "Register"
  },
  {
    path: "/login",
    component: Login,
    name: "Login"
  },
  {
    path: "/index",
    component: Index,
    name: "Index"
  },
  {
    path: "/items",
    component: Items,
    name: "Items"
  }
];

const router = new VueRouter({
  routes // short for `routes: routes`
});

// nav guard to prompt user to login
router.beforeEach((to, from, next) => {
  if (to.name === "Items" && store.getters.uid === null) {
    next({ name: "Login" });
  } else {
    next();
  }
});
// done vue router

// Add a response interceptor
axios.interceptors.response.use(
  function(response) {
    // Do something with response data
    return response;
  },
  function(error) {
    // Logout if we get unauth
    if (error.response.status === 401) {
      store.commit("logout");
      router.push("login");
    }
    if (error.response.status === 403) {
      store.commit("logout");
      router.push("login");
    }
    if (error.response.status === 422) {
      store.commit("logout");
      router.push("login");
    }
    return Promise.reject(error);
  }
);

// end axios interceptors
new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate() {
    this.$store.commit("initStore");
  }
}).$mount("#app");
