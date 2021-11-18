<template>
  <div>
    <h1>Signup</h1>
    <div>
      <label for="username">name:</label>
      <input
        type="text"
        id="username"
        v-model="credentials.username"
        @keyup.enter="signup"
      />
    </div>
    <div>
      <label for="nickname">nickname:</label>
      <input
        type="text"
        id="nickname"
        v-model="credentials.nickname"
        @keyup.enter="signup"
      />
    </div>
    <div>
      <label for="email">email:</label>
      <input
        type="text"
        id="email"
        v-model="credentials.email"
        @keyup.enter="signup"
      />
    </div>
    <div>
      <label for="password">password:</label>
      <input
        type="text"
        id="password"
        v-model="credentials.password"
        @keyup.enter="signup"
      />
    </div>
    <div>
      <label for="passwordConfirmation">passwordConfirmation:</label>
      <input
        type="text"
        id="passwordConfirmation"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      />
    </div>
    <button @click.stop="signup">Signup</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Signup",
  data: function () {
    return {
      credentials: {
        username: null,
        nickname: null,
        email:null,
        password: null,
        paswordConfirmation: null,

      },
    };
  },
  methods: {
    signup: function () {
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/accounts/signup/",
        data: this.credentials,
      })
        .then(() => {
          axios({
            method: "POST",
            url: "http://127.0.0.1:8000/accounts/api-token-auth/",
            data: this.credentials,
          })
            .then((res) => {
              localStorage.setItem("jwt", res.data.token);
              this.$router.push({ name: "Home" });
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
