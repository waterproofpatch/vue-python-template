<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <p v-if="itemId">Item {{itemId}}</p>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Item",
  props: ['itemId'],
  data() {
    return {
      error: null
    };
  },
  mounted() {
    if (this.$store.state.uid == null) {
      this.$router.push("login");
      return;
    }
  },
  methods: {
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
