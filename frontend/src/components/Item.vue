<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <p v-if="item">Item ID: {{ item.id }}</p>
    <p v-if="item">User ID: {{ item.user_id }}</p>
    <p v-if="item">Json Field 1: {{ item.jsonfield1 }}</p>
    <p v-if="item">Json Field 1 Attribute A: {{ item.jsonfield1.attributeA }}</p>
    <p v-if="item">Json Field 1 Attribute B: {{ item.jsonfield1.attributeB }}</p>
    <p v-if="item">Created on: {{ item.created_on }}</p>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Item",
  props: ["item"],
  data() {
    return {
      error: null
    };
  },
  mounted() {
    console.log("i am on item " + this.$route.params.id);
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
