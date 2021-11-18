<template>
  <div>
    <button @click="getMovie">임시버튼</button>
    <input type="text" @keyup.enter="getSearch" v-model="query" />
    <hr />
    {{ movies }}
    {{ result}}
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "MovieList",
  data: function () {
    return {
      query: null,
      movies: [],
      result: [],
    };
  },
  methods: {
    ...mapActions(["getMovieList", "search"]),
    getMovie: function () {
      this.getMovieList()
        .then((res) => {
          console.log(res);
          this.movies = res;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getSearch: function () {
      this.search(this.query)
        .then((res) => {
          this.result = res;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
