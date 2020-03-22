<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <h2 v-if="success">Success: {{ success }}</h2>
    <center>
      <div v-if="!showAddComponent && !selectedItemId">
        <button
          class="button-add"
          v-on:click="showAddComponent = true"
        >
          Add
        </button>
      </div>
      <div v-else>
        <button
          class="button-add"
          v-on:click="
            showAddComponent = false;
            selectedItemId = false;
          "
        >
          Back
        </button>
      </div>
    </center>
    <p v-if="items.length == 0">Nothing here!</p>

    <section
      v-if="!showAddComponent && !selectedItemId"
      class="cards"
    >
      <div
        v-for="item in items"
        v-bind:key="item.id"
        class="card"
        v-on:click="selectItem(item.id)"
      >
        <div class="card-header">
          <div>
            header
          </div>
          <div>
            delete
          </div>
        </div>
        <div class="card-main">
          <div class="main-description">
            {{ item }}
          </div>
        </div>
      </div>
    </section>

    <AddItem
      v-on:add-item="addItem"
      v-if="showAddComponent"
    />
    <Item
      v-on:delete-item="deleteItem"
      v-if="selectedItemId"
      v-bind:item-id="selectedItemId"
    />

    <!-- <p align="center"><button v-on:click="addItem">Add</button></p> -->
  </div>
</template>

<script>
/* eslint-disable */
import AddItem from "./AddItem.vue";
import Item from "./Item.vue";
export default {
  name: "Items",
  components: {
    AddItem,
    Item
  },
  props: {},
  data() {
    return {
      items: [],
      showAddComponent: false,
      selectedItemId: null,
      error: null,
      success: null
    };
  },
  mounted() {
    // if (this.$store.state.uid == null) {
    //   this.$router.push("login");
    //   return;
    // }
    this.getItems();
  },
  methods: {
    getItems: function() {
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
    addItem: function(item) {
      this.axios
        .post("/api/items", {
          field1: item.field1,
          jsonfield1: item.attributes
        })
        .then(response => {
          console.log("got response " + response);
          if (response.status == 200) {
            this.success = "Item added.";
            this.getItems();
            this.showAddComponent = false;
            this.error = null;
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
    },
    deleteItem: function(id) {
      this.axios
        .delete("/api/items?id=" + id)
        .then(response => {
          if (response.status == 200) {
            this.success = "Item removed.";
            this.getItems();
            this.error = null;
            this.selectedItemId = null;
          } else {
            this.success = null;
            console.log("some unexpected response");
          }
        })
        .catch(error => {
          console.log("error return code was: " + error.response.status);
          if (error.response.status == 400) {
            this.error = error.response.data.error;
            this.success = null;
          } else {
            this.error = error.response.status;
            this.success = null;
          }
        })
        .finally(response => {});
    },
    selectItem: function(id) {
      this.selectedItemId = id;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@media screen and (min-width: 40em) {
  .card {
    max-width: calc(75% - 1em);
  }
}
@media screen and (min-width: 60em) {
  .card {
    max-width: calc(25% - 1em);
  }
}
.cards {
  justify-content: space-between;
  display: flex;
  flex-wrap: wrap;
}

.card {
  width: 250px; /* Set width of cards */
  display: flex; /* Children use Flexbox */
  flex-direction: column; /* Rotate Axis */
  border: 1px solid #409fbf; /* Set up Border */
  border-radius: 4px; /* Slightly Curve edges */
  overflow: hidden; /* Fixes the corners */
  margin: 5px; /* Add space between cards */
  background: white;
  /* box-shadow: 1px 2px rgba(0, 0, 0, 0.1); */
}

.card-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: white;
  font-weight: 600;
  /* border-bottom: 1px solid #409fbf; */
  background-color: #409fbf;
  padding: 5px 10px;
}

.card-main {
  display: flex; /* Children use Flexbox */
  flex-direction: column; /* Rotate Axis to Vertical */
  justify-content: center; /* Group Children in Center */
  align-items: center; /* Group Children in Center (on cross axis) */
  padding: 15px 0; /* Add padding to the top/bottom */
}

.main-description {
  color: black;
  text-align: center;
}
</style>
