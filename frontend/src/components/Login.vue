<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <div class="login-container">
      <p>test@gmail.com | passwordpassword</p>
      <form class="form form-login">
        <div class="form-field">
          <input placeholder="Email" type="text" v-model="email">
        </div>
        <div class="form-field">
        <input placeholder="Password" type="password" v-model="password">
        </div>
        <div class="form-field">
        <input class="btn" type="submit" value="Login" v-on:click.prevent="doLogin">
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
          this.$store.commit("login", response.data.uid, response.data.email);
          this.$router.push(this.prevRoute);
        })
        .catch(error => {
          console.log(error.response.data.error);
          this.error = error.response.data.error;
        })
        .finally(response => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-container {
  align-items: center;
  display: flex;
  flex-direction: column;
}
.form-login {
  width: 450px;
  display: flex;
  flex-direction: column;
}
.form-login input[type="text"],
.form-login input[type="password"] {
  border: 1px solid #888;
}
.form-login input[type="text"],
.form-login input[type="password"],
.form-login input[type="submit"] {
  border-radius: 0.25rem;
  padding: 1rem;
  color: #3A3F44;  
  background-color: #ffffff;
  width: 100%;
}
.form-login input[type="text"]:focus,
.form-login input[type="text"]:hover,
.form-login input[type="password"]:focus,
.form-login input[type="password"]:hover {
  background-color: #eeeeee;
}
.form-login input[type="submit"] {
  background-color: #409fbf;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}
.form-login input[type="submit"]:focus,
.form-login input[type="submit"]:hover {
  background-color: black;
}
.form-field {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  margin-bottom: 2rem;
}
input {
  border: 0;
  color: inherit;
  font: inherit;
  margin: 0;
  outline: 0;
  padding: 0;
  -webkit-transition: background-color .3s;
  transition: background-color .3s;
}
</style>
