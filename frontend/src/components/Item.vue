<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <p v-if="itemId">Item {{ itemId }}</p>
    <button class="button-delete" v-on:click="deleteItem(itemId)">
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
  mounted() {
    if (this.$store.state.uid == null) {
      this.$router.push("login");
      return;
    }
  },
  methods: {
    deleteItem: function(id) {
      console.log("called delete");
      this.axios
        .delete("/api/items", {
          id: id
        })
        .then(response => {
          if (response.status == 200) {
            this.success = "Item removed.";
          } else {
            this.success = null;
          }
        })
        .catch(error => {
          if (error.response.status == 400) {
            this.error = error.response.data.error;
            this.success = null;
          } else {
            this.error = error.response.status;
            this.success = null;
          }
        })
        .finally(response => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
