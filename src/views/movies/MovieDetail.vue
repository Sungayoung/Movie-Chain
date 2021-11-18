<template>
  <div>
    <button @click="getMovie()">영화불러오기</button>
    {{ movie }}

    <hr />
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "MovieDetail",
  data: function () {
    return {
      movie: null,
    };
  },
  props: { movieId: Number },
  methods: {
    ...mapActions(["getMovieDetail"]),
    getMovie: function () {
      this.getMovieDetail(this.movieId)
        .then((res) => {
          this.movie = res;
        })
        .catch((err) => {
          console.log(err);
        });
  },
  mounted: function () {
      this.getMovie()
    },
  },
};
</script>

<style></style>
