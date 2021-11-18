import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {
    getMovieList: function ({ commit }, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",
          url: `${process.env.VUE_APP_MCS_URL}/movies/`,
          headers: { Authorization: `JWT ${token}` },
          params,
        })
          .then((res) => {
            // console.log(res.data)
            resolve(res.data);
          })
          .catch((err) => {
            // console.log(err.data)
            reject(err.data);
          });
      });
    },
    search: function ({ commit }, query) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",
          url: `${process.env.VUE_APP_MCS_URL}/movies/search/`,
          headers: { Authorization: `JWT ${token}` },
          params: {
            query: query,
          },
        })
          .then((res) => {
            // console.log(res.data);
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    getMovieDetail: function ({ commit }, moviePk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",

          url: `${process.env.VUE_APP_MCS_URL}/movies/${moviePk}/`,
          headers: { Authorization: `JWT ${token}` },
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    getActorList: function ({ commit }, moviePk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",
          url: `${process.env.VUE_APP_MCS_URL}/movies/${moviePk}/actors/`,
          headers: { Authorization: `JWT ${token}` },
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    getCrewList: function ({ commit }, moviePk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",
          url: `${process.env.VUE_APP_MCS_URL}/movies/${moviePk}/crews/`,
          headers: { Authorization: `JWT ${token}` },
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    getReview: function ({ commit }, movie_pk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/${movie_pk}/reviews/`,
          headers: { Authorization: `JWT ${token}` },
          method: "get",
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    createReview: function ({ commit }, movie_pk, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/${movie_pk}/reviews/`,
          headers: { Authorization: `JWT ${token}` },
          method: "get",
          params,
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    updateReview: function ({ commit }, review_pk, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "put",
          params,
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    deleteReview: function ({ commit }, review_pk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "delete",
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    getComment: function ({ commit }, review_pk) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "get",
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    createComment: function ({ commit }, review_pk, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "post",
          params,
        })
          .then((res) => {
            return res.data;
          })
          .catch((err) => {
            return err.data;
          });
      });
    },
    updateComment: function ({ commit }, review_pk, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "put",
          params,
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    createComment: function ({ commit }, review_pk, params) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          url: `${process.env.VUE_APP_MCS_URL}/movies/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${token}` },
          method: "post",
          params,
        })
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
  },
  modules: {},
});
