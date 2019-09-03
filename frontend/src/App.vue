<template>
  <div id="app">
    App.vue<br>
    Login state: {{$store.state.uid != null}}<br>
    <ul>
      <li v-if="$store.state.uid == null">
        <router-link to="/login">Login</router-link><br>
      </li>
      <li v-if="$store.state.uid == null">
        <router-link to="/register">Register</router-link><br>
      </li>
      <li v-if="$store.state.uid != null">
        <router-link
          to="/index"
          @click.native="doLogout"
        >Logout</router-link><br>
      </li>
      <li>
        <router-link to="/index">Home</router-link>
      </li>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {},
  methods: {
    doLogout() {
      this.axios
        .post("/api/logout", {})
        .then(() => {
          this.$store.commit("logout");
        })
        .catch(() => {})
        .finally(() => {});
    }
  }
};
</script>

<style>
</style>
