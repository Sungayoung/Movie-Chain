<template>
  <div>
    <h1>리뷰리뷰</h1>
    <input type="text" v-model="content">
    <input type="text" v-model="rank">
    <button @click='submitReview'></button>
  </div>
</template>

<script>
import {mapActions} from 'vuex'

export default {
name:'Review',
data: function () {
  return {
    content: null,
    rank: null,
  }
},
props: {
  movieId:Number,
},
methods: {
  ...mapActions(['createReview']),
  submitReview: function () {
    const data = {
      content:content,
      rank:rank,
    }
    

    })
  }
}



}
</script>

<style>

</style>