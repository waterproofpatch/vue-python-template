<template>
  <div>
    <h2 v-if="error">Error: {{error}}</h2>
    <p>
    <div class="form-container">
      <form class="form form-item">
        <div class="form-field">
          <input placeholder="Field1" type="text" v-model="newItem.field1">
        </div>
        <div class="form-field">
          <input placeholder="JsonFieldAttributeA" type="text" v-model="newItem.attributes.attributeA">
        </div>
        <div class="form-field">
          <input placeholder="JsonFieldAttributeB" type="text" v-model="newItem.attributes.attributeB">
        </div>
        <div class="form-field">
        <input class="btn" type="submit" value="Add" v-on:click.prevent="addItem">
        </div>
      </form>
    </div>
  </p>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Privileged",
  props: {},
  data() {
    return {
      newItem: {
        field1: "",
        attributes: {
          attributeA: "",
          attributeB: "",
        }
      },
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
    addItem() {
      this.axios
        .post("/api/items", {
          field1: this.newItem.field1,
          jsonfield1: this.newItem.attributes
        })
        .then(response => {
          console.log("got response " + response);
        })
        .catch(error => {
          if (error.response.status == 400) {
            this.error = error.response.data.error;
          }
          else {
            this.error = error.response.status;
          }
        })
        .finally(response => {});
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.form-item {
  width: 450px;
  display: flex;
  flex-direction: column;
}
.form-item input[type="text"],
.form-item input[type="password"] {
  border: 1px solid #888;
}
.form-item input[type="text"],
.form-item input[type="password"],
.form-item input[type="submit"] {
  border-radius: 0.25rem;
  padding: 1rem;
  color: #3A3F44;  
  background-color: #ffffff;
  width: 100%;
}
.form-item input[type="text"]:focus,
.form-item input[type="text"]:hover,
.form-item input[type="password"]:focus,
.form-item input[type="password"]:hover {
  background-color: #eeeeee;
}
.form-item input[type="submit"] {
  background-color: #409fbf;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}
.form-item input[type="submit"]:focus,
.form-item input[type="submit"]:hover {
  background-color: black;
}
.form-field {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  margin-bottom: 2rem;
}
input {
  border: 0;
  color: inherit;
  font: inherit;
  margin: 0;
  outline: 0;
  padding: 0;
  -webkit-transition: background-color .3s;
  transition: background-color .3s;
}
</style>
