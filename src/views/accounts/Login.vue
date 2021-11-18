<template>
  <div>
    <h1>Login</h1>
    <div>
      <label for="username">name:</label>
      <input
        type="text"
        id="username"
        v-model="credentials.username"
        @keyup.enter="login"
      />
    </div>
    <div>
      <label for="password">password:</label>
      <input
        type="text"
        id="password"
        v-model="credentials.password"
        @keyup.enter="login"
      />
    </div>
    <button @click.stop="login">Login</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      },
    };
  },
  methods: {
    login: function () {
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/accounts/api-token-auth/",
        data: this.credentials,
      })
        .then((res) => {
          console.log(res);
          localStorage.setItem("jwt", res.data.token);
          this.$router.push({ name: "Home" });
          this.$emit("login");
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
