<template>
  <div id="app">
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
form {
  margin:10px;
  padding:20px;
  background:lightgray;
  width:75%;
}
input {
 color: #333333;
 font-family: "Helvetica Neue", Arial, sans-serif;
 font-size: 16px;
 font-weight: 300;
 line-height: 1.5625;
 margin-bottom: 15px;
}
input.btn {
  color: white;
  background-color: black;
}
</style>
