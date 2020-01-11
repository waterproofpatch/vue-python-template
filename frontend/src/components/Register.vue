<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <div class="form-container">
      <p>Register</p>
      <form class="form form-auth">
        <div class="form-field">
          <input placeholder="Email" type="text" v-model="email">
       </div>
        <div class="form-field">
          <input placeholder="Password" type="password" v-model="password">
       </div>
        <div class="form-field">
        <input placeholder="Confirm Password" type="password" v-model="passwordConfirmation">
       </div>
        <div class="form-field">
          <input class="btn" type="submit" value="Register" v-on:click.prevent="doRegister">
       </div>
      </form>
    </div>
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
          this.$store.commit("login", 
            {uid: response.data.uid, email: response.data.email}
          );
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
