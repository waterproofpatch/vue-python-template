<template>
  <div id="app">
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
      <li>
        <router-link to="/privileged">Privileged</router-link>
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
div {
  color: #333333;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  font-weight: 300;
  line-height: 1.5625;
  margin-bottom: 15px;
}
</style>
