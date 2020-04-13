<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <div v-if="item">
      <p><a
          href="#"
          v-on:click="$router.push({name: 'Items'})"
        >Back</a></p>
      <p v-if="item">Item ID: {{ item.id }}</p>
      <p v-if="item">User ID: {{ item.user_id }}</p>
      <p v-if="item">Json Field 1: {{ item.jsonfield1 }}</p>
      <p v-if="item">Json Field 1 Attribute A: {{ item.jsonfield1.attributeA }}</p>
      <p v-if="item">Json Field 1 Attribute B: {{ item.jsonfield1.attributeB }}</p>
      <p v-if="item">Created on: {{ item.created_on }}</p>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      error: null,
      item: null
    };
  },
  mounted() {
    console.log("I am on item " + this.$route.params.id);
    this.getItems(this.$route.params.id);
  },
  methods: {
    getItems: function(id) {
      this.axios
        .get("/api/items?id=" + id)
        .then(response => {
          this.item = response.data[0];
        })
        .catch(error => {
          this.item = null;
          this.error = error.response.data.error;
        })
        .finally(() => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
