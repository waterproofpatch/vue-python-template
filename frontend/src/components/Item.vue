<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <p v-if="itemId">Item {{ itemId }}</p>
    <button
      class="button-delete"
      v-on:click="$emit('delete-item', itemId)"
    >
      Remove
    </button>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Item",
  props: ["itemId"],
  data() {
    return {
      error: null
    };
  },
  mounted() {},
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
