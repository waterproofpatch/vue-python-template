<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <h1>Register</h1>
    <form class="form1">
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
        placeholder="Confirm Password"
        type="password"
        v-model="passwordConfirmation"
      >
      <input
        class="btn"
        type="submit"
        value="Register"
        v-on:click.prevent="doRegister"
      >
    </form>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Register",
  props: {},
  data() {
    return {
      error: null,
      email: "",
      password: "",
      passwordConfirmation: ""
    };
  },
  mounted() {},
  methods: {
    doRegister() {
      this.axios
        .post("/api/register", {
          email: this.email,
          password: this.password,
          passwordConfirmation: this.passwordConfirmation
        })
        .then(response => {
          this.$store.commit("login", response.data.uid, response.data.email);
          this.$router.push("index");
        })
        .catch(error => {
          this.error = error.response.data.error;
          console.log(error.response.data.error);
        })
        .finally(response => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
