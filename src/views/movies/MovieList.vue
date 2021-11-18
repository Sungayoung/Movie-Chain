<template>
  <div>
    <button @click="getMovie">임시버튼</button>
    <input type="text" @keyup.enter="getSearch" v-model="query" />
    <hr />
    <div v-for="(movie, idx) in movies" :key="idx"
    @click="moveDetail(movie.id)">
    {{ movie.id }}
    </div>
    <div v-for="(result, idx) in results" :key="idx">
      {{ result }}
    </div>
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
      results: [],
    };
  },
  methods: {
    ...mapActions(["getMovieList", "search"]),
    getMovie: function () {
      const params = {
        filter_by: 'all',
      }
      this.getMovieList(params)
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
          this.results = res;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    moveDetail: function (id) {
      this.$router.push({
        name: 'MovieDetail',
        params: {
          movieId: id
        }
      })
    }
  },
};
</script>

<style></style>
