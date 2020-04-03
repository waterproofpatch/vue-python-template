<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <h2 v-if="success">Success: {{ success }}</h2>
    <!-- show the 'add' button -->
    <center>
      <div v-if="showAddComponent || selectedItem">
        <a href="#">
          <span
            v-on:click="showAddComponent = false;
            selectedItem=false;"
            style="color: var(--button-bg-color);"
          >
            <font-awesome-icon
              size="3x"
              :icon="['fas', 'arrow-left']"
            />
          </span></a>
      </div>
    </center>

    <!-- print a message if no items are availabel -->
    <p v-if="items.length == 0">Nothing here!</p>

    <!-- show each item -->
    <section
      v-if="!showAddComponent && !selectedItem"
      class="cards"
    >
      <div
        v-for="item in items"
        v-bind:key="item.id"
        v-on:click="selectedItem = item"
        class="card"
      >
        <div class="card-header">
          <div>
            {{item.id}}
          </div>
          <div>
            <a
              v-on:click="deleteItem(item.id)"
              href="#"
            >
              <span style="color: white;">
                <font-awesome-icon :icon="['fas', 'trash']" /></span>
            </a>
          </div>
        </div>
        <div class="card-main">
          <div class="main-description">
            {{ item }}
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div>
            <!-- NA -->
          </div>
          <div>
            <a href="#">
              <span
                v-on:click="showAddComponent = true"
                style="color: var(--main-bg-color);"
              >
                <font-awesome-icon :icon="['fas', 'plus']" />
              </span></a>
          </div>
        </div>
        <div class="card-main">
          <div class="main-description">
            <!-- Add -->
          </div>
        </div>
      </div>
    </section>

    <AddItem
      v-on:add-item="addItem"
      v-if="showAddComponent"
    />
    <Item
      v-if="selectedItem"
      v-bind:item="selectedItem"
    />

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
      selectedItem: null,
      error: null,
      success: null
    };
  },
  mounted() {
    console.log("have item: " + this.$route.params.id);
    if (this.$route.params.id != null) {
      console.log("specifying item: " + this.$route.params.id);
    }
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
            this.selectedItem = null;
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
  /* justify-content: space-between; */
  display: flex;
  flex-wrap: wrap;
  padding-top: 20px;
}

.card {
  width: 250px; /* Set width of cards */
  height: 250px;
  display: flex; /* Children use Flexbox */
  flex-direction: column; /* Rotate Axis */
  border-radius: 4px; /* Slightly Curve edges */
  overflow: hidden; /* Fixes the corners */
  margin: 5px; /* Add space between cards */
  background: white;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
}
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
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
