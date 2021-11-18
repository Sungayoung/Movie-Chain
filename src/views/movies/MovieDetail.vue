<template>
  <div>
    <Review/>
    {{ movie }}
    <hr />
  </div>
</template>

<script>
import { mapActions } from "vuex";
import Review from "./Review.vue"

export default {
  name: "MovieDetail",
  data: function () {
    return {
      movie: null,
    };
  },
  components: {
    Review,
  },
  props: { movieId: Number },
  mounted: function () {
    this.getMovie();
  },
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
  },
};
</script>

<style></style>
