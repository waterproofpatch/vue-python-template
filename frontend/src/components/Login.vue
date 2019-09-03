<template>
  <div>
    Register
    <form>
      <input
        placeholder="Email"
        type="text"
        v-model="email"
      >
      <input
        placeholder="Password"
        type="password"
        v-model="password"
      >
      <input
        type="submit"
        v-on:click="doLogin"
      >
    </form>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Login",
  props: {},
  data() {
    return {
      email: "",
      password: ""
    };
  },
  mounted() {},
  methods: {
    doLogin() {
      this.axios
        .post("/api/login", {
          email: this.email,
          password: this.password
        })
        .then(response => {
          console.log("OK");
        })
        .catch(error => {
          console.log("Problem");
        })
        .finally(response => {
          console.log("Done.");
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
