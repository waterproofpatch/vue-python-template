<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <div class="form-container">
      <p>test@gmail.com | passwordpassword</p>
      <form class="form form-auth">
        <div class="form-field">
          <input
            placeholder="Email"
            type="text"
            v-model="email"
          >
        </div>
        <div class="form-field">
          <input
            placeholder="Password"
            type="password"
            v-model="password"
          >
        </div>
        <div class="form-field">
          <input
            class="btn"
            type="submit"
            value="Login"
            v-on:click.prevent="doLogin"
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Login",
  props: {},
  data() {
    return {
      error: null,
      email: "",
      password: "",
      prevRoute: null
    };
  },
  // TODO move this to main
  beforeRouteEnter(to, from, next) {
    next(vm => {
      console.log("beforeRouterEnter: " + from.path);
      vm.prevRoute = from;
    });
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
          this.$store.commit("login", {
            uid: response.data.uid,
            email: response.data.email
          });
          this.$router.push(this.prevRoute);
        })
        .catch(error => {
          if (error.response.status == 400) {
            this.error = error.response.data.error;
          } else if (error.response.status == 401) {
            this.error = error.response.data.error;
          } else {
            this.error = error.response.status;
          }
        })
        .finally(response => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
