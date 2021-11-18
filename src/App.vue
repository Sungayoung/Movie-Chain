<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <div v-if="isLogin">
        <router-link @click.native="logout" to="#">Logout</router-link> | 
        <router-link :to="{name: 'MovieList'}">MovieList</router-link>
      </div>
      <div v-else>
        <router-link :to="{ name: 'Signup' }">Signup</router-link> |
        <router-link :to="{ name: 'Login' }">Login</router-link> |
      </div>
    </div>
    <router-view @login="login" />
  </div>
</template>

<script>
export default {
  name: "App",
  data: function () {
    return {
      isLogin: false,
    };
  },
  methods: {
    logout: function () {
      this.isLogin = false;
      localStorage.removeItem("jwt");
      this.$router.push({ name: "Login" });
    },
    login: function () {
      this.isLogin = true;
    }
  },
  created: function () {
    const token = localStorage.getItem("jwt");
    if (token) {
      this.isLogin = true;
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
