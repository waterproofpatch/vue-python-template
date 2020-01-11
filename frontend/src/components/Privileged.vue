<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>

    <p v-if="!showAddComponent">
      <a href="#" v-on:click="showAddComponent=true">Add</a>
    </p>
    <p v-else>
      <a href="#" v-on:click="showAddComponent=false">Back</a>
    </p>

    <section v-if="!showAddComponent" class="cards">
      <div v-for="item in items" v-bind:key="item.id" class="card">
        <div class="card-header">header</div>
        <div class="card-main">
          <div class="main-description">
          {{item}}
          </div>
        </div>
      </div>
    </section>

    <AddItem v-if="showAddComponent"/>

    <!-- <p align="center"><button v-on:click="addItem">Add</button></p> -->
  </div>
</template>

<script>
/* eslint-disable */
import AddItem from './AddItem.vue'
export default {
  name: "Privileged",
  components: {
    AddItem
  },
  props: {},
  data() {
    return {
      items: [],
      showAddComponent: false,
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
      .get("/api/items") .then(response => {
        this.items = response.data;
      })
      .catch(error => {
        this.items = [];
        this.error = error.response.data.error;
      })
      .finally(() => {});
  },
  methods: {
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@media screen and (min-width: 40em) {
    .card {
       max-width: calc(75% -  1em);
    }
}
@media screen and (min-width: 60em) {
    .card {
        max-width: calc(25% - 1em);
    }
}
.cards {
  justify-content: space-between;
  padding:20px;
  display: flex;
  flex-wrap: wrap;
 }
 
.card {
  width: 250px;                 /* Set width of cards */
  display: flex;                /* Children use Flexbox */
  flex-direction: column;       /* Rotate Axis */
  border: 1px solid #409fbf;    /* Set up Border */
  border-radius: 4px;           /* Slightly Curve edges */
  overflow: hidden;             /* Fixes the corners */
  margin: 5px;                  /* Add space between cards */
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
  display: flex;              /* Children use Flexbox */
  flex-direction: column;     /* Rotate Axis to Vertical */
  justify-content: center;    /* Group Children in Center */
  align-items: center;        /* Group Children in Center (on cross axis) */
  padding: 15px 0;            /* Add padding to the top/bottom */
}

.main-description {
  color: black;
  text-align: center;
}
</style>
