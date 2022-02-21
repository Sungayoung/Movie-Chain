<template>
  <div>
    <input type="text" v-model="query" @keyup.enter="querySearch()">
    <p>{{ movieInfo }}</p>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'Review',
  data: function () {
    return {
      query: null,
      movieInfo: []
    }
  },
  methods: {
    ...mapActions([
      'search'
    ]),
    querySearch: function () {
      this.search(this.query).then( res => {
        console.log(res)
        this.movieInfo = res
      })
    }
  }
}
</script>

<style>

</style>