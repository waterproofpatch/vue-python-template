<template>
  <div class="header">
    <div class="banner">
      MySite. Login state: {{$store.state.uid != null}}
    </div>
    <nav>
      <ul>
        <li><router-link to="/index">Home</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/index" 
            @click.native="doLogout">Logout</router-link></li>
        <li><router-link v-if="$store.state.uid != null" 
            to="/privileged">Privileged</router-link></li>
      </ul>
    </nav>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Header",
  props: {},
  data() {
    return {};
  },
  mounted() {},
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: #333333;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  font-weight: 300;
  line-height: 1.5625;
  margin-bottom: 15px;
}
nav {
  align-self: center;
  margin: 0 0.8em 0 0;
}
.header ul {
  display: flex;
  flex-flow: row wrap;
  list-style-type: none;
}
.header ul li {
  padding: 0 1.4em 0 0;
  font-size: 0.9em;
}
</style>
