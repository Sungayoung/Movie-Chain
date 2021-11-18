import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {
    getMovieList: function (
      { commit },
      orderBy = "-id",
      filterBy = "all",
      filterId = null
    ) {
      commit;
      const token = localStorage.getItem("jwt");
      return new Promise((resolve, reject) => {
        axios({
          method: "GET",
          url: `${process.env.VUE_APP_MCS_URL}/movies/`,
          headers: { Authorization: `JWT ${token}` },
          params: {
            order_by: orderBy,
            filter_by: filterBy,
            filter_id: filterId,
          },
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
  },
  modules: {},
});
