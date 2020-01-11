<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <ul v-if="items.length > 0">
      <li v-for="item in items" v-bind:key=item.id >
        Item: {{item}}
      </li>
    </ul>
    <p v-if="items.length == 0 && showAddComponent==false">Nothing here! 
      <a href="#" v-on:click="showAddComponent=true">Add your first item.</a>
    </p>
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
button {
  display: flex;
  border-radius: 0.25rem;
  border: none;
  padding: 1rem;
  font-weight: bold;
  color: white;  
  background-color: #409fbf;
  width: 60px;
  -webkit-transition: background-color .3s;
  transition: background-color .3s;
}
button:hover {
  display: flex;
  border-radius: 0.25rem;
  padding: 1rem;
  color: white;  
  background-color: #3A3F44;
  width: 60px;
}
</style>
