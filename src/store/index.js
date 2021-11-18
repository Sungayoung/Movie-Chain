import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
    getReview: function ({ commit }, movie_pk) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/${movie_pk}/reviews/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'get',
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    createReview: function ({ commit }, movie_pk, params) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/${movie_pk}/reviews/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'get',
          params,
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    updateReview: function ({ commit }, review_pk, params) {
      
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'put',
          params,
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    deleteReview: function ({ commit }, review_pk) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'delete',
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    getComment: function({ commit }, review_pk) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'get',
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    createComment: function({ commit }, review_pk, params) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'post',
          params,
        })
        .then( res => {
          return res.data
        })
        .catch( err => {
          return err.data
        })
      })
    },
    updateComment: function({ commit }, review_pk, params) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'put',
          params,
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
    createComment: function({ commit }, review_pk, params) {
      commit
      const token = localStorage.getItem('jwt')
      return new Promise (( resolve, reject ) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: 'post',
          params,
        })
        .then( res => {
          resolve(res.data)
        })
        .catch( err => {
          reject(err.data)
        })
      })
    },
  },
  modules: {
  }
})
