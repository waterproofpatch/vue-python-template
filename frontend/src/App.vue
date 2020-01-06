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
a {
  color: white;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
div.container {
  display: flex;
  flex-direction: column;
  width: 800px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-weight: 300;
  margin: auto;
}
</style>
