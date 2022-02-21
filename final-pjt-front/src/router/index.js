import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Signup from "../views/accounts/Signup.vue";
import Login from "../views/accounts/Login.vue";
import MovieList from "../views/movies/MovieList";
import MovieDetail from "../views/movies/MovieDetail";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/accounts/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/accounts/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/movielist",
    name: "MovieList",
    component: MovieList,
  },
  {
    path: "/moviedetail/:movieId",
    name: "MovieDetail",
    component: MovieDetail,
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
