<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    Privileged<br><br>
    {{items.length}} items:<br>
    <ul v-if="items.length > 0">
      <li
        v-for="item in items"
        v-bind:key=item.id
      >
        Item: {{item}}
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Privileged",
  props: {},
  data() {
    return {
      items: [],
      error: null
    };
  },
  mounted() {
    if (this.$store.state.uid == null) {
      this.$router.push("login");
      return;
    }
    this.axios
      .get("/api/items")
      .then(response => {
        this.items = response.data;
      })
      .catch(error => {
        this.items = [];
        this.error = error.response.data.error;
      })
      .finally(() => {});
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
