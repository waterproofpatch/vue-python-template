<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>

    <p v-if="!showAddComponent && !selectedItemId">
      <a href="#" v-on:click="showAddComponent = true">Add</a>
    </p>
    <p v-else>
      <a
        href="#"
        v-on:click="
          showAddComponent = false;
          selectedItemId = false;
        "
        >Back</a
      >
    </p>
    <p v-if="items.length == 0">Nothing here!</p>

    <section v-if="!showAddComponent && !selectedItemId" class="cards">
      <div
        v-for="item in items"
        v-bind:key="item.id"
        class="card"
        v-on:click="selectItem(item.id)"
      >
        <div class="card-header">header</div>
        <div class="card-main">
          <div class="main-description">
            {{ item }}
          </div>
        </div>
      </div>
    </section>

    <AddItem v-if="showAddComponent" />
    <Item v-if="selectedItemId" v-bind:item-id="selectedItemId" />

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
      error: null
    };
  },
  mounted() {
    console.log(this.showAddComponent);
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
  methods: {
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
  box-shadow: 1px 2px rgba(0, 0, 0, 0.1);
}

.card-header {
  color: white;
  text-align: center;
  font-weight: 600;
  border-bottom: 1px solid #409fbf;
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
