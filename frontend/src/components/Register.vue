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
        placeholder="Confirm Password"
        type="password"
        v-model="passwordConfirmation"
      >
      <input
        type="submit"
        v-on:click="doRegister"
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
