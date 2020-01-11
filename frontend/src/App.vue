<template>
  <div id="app" class="container">
    <Header></Header>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: "app",
  components: {
    Header
  },
  methods: {}
};
</script>

<style>
@import './assets/theme.css';
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
a:visited {
  text-decoration: none;
}
div.container {
  display: flex;
  background: #f7f7f7;
  flex-direction: column;
  width: 800px;
  color: black;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-weight: 300;
  margin: auto;
}
.form-container {
  align-items: center;
  display: flex;
  flex-direction: column;
}
.form-auth {
  width: 450px;
  display: flex;
  flex-direction: column;
}
.form-auth input[type="text"],
.form-auth input[type="password"] {
  border: 1px solid #888;
}
.form-auth input[type="text"],
.form-auth input[type="password"],
.form-auth input[type="submit"] {
  border-radius: 0.25rem;
  padding: 1rem;
  color: #3A3F44;  
  background-color: #ffffff;
  width: 100%;
}
.form-auth input[type="text"]:focus,
.form-auth input[type="text"]:hover,
.form-auth input[type="password"]:focus,
.form-auth input[type="password"]:hover {
  background-color: #eeeeee;
}
.form-auth input[type="submit"] {
  background-color: #409fbf;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}
.form-auth input[type="submit"]:focus,
.form-auth input[type="submit"]:hover {
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
