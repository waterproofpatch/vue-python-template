<template>
  <div id="app">
    App.vue<br>
    <router-link to="/login">Login</router-link><br>
    <router-link to="/register">Register</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {}
};
</script>

<style>
</style>
