<template>
  <div>
    <h2 v-if="error">Error: {{ error }}</h2>
    <div class="form-container">
      <form class="form form-item">
        <div class="form-field">
          <input
            type="file"
            class="btn"
            @change="changeFile"
          />
        </div>
        <div class="form-field">
          <input
            class="btn"
            type="submit"
            value="Add"
            v-on:click.prevent="uploadFile()"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Images",
  props: {},
  data() {
    return {
      file: null,
      error: null
    };
  },
  mounted() {},
  methods: {
    uploadFile: function() {
      const formData = new FormData();
      formData.append("theFile", this.file, this.file.name);
      this.axios
        .post("/api/files", formData, {
          onUploadProgress: progressEvent => {
            console.log(
              "loaded " +
                progressEvent.loaded +
                ", total " +
                progressEvent.total
            );
          }
        })
        .then(response => {
          console.log("done sending file");
        })
        .catch(error => {
          if (error.response.status == 400) {
            this.error = error.response.data.error;
            this.success = null;
          }
        });
    },
    changeFile: function(event) {
      console.log("setting this file to " + event.target.files[0]);
      this.file = event.target.files[0];
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
  color: var(--input-border-color);
  background-color: #ffffff;
  width: 100%;
}
.form-item input[type="text"]:focus,
.form-item input[type="text"]:hover,
.form-item input[type="password"]:focus,
.form-item input[type="password"]:hover {
  background-color: var(--input-hover-bg-color);
}
.form-item input[type="submit"] {
  background-color: var(--button-bg-color);
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
  -webkit-transition: background-color 0.3s;
  transition: background-color 0.3s;
}
</style>
