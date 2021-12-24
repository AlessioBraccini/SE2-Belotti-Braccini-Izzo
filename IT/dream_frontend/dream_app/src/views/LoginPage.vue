<template>

  <img src="../assets/dramLogo.png" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">

    <input type="email" required v-model="email" placeholder="Email" class="textInput">

    <input type="password" required v-model="password" placeholder="Password" class="textInput">

    <div class="submit">
      <button class="actionButton localButton">Log In</button>
    </div>
  </form>
  <button class="actionButton localButton" @click="redirectSignUp">Sign Up</button>
</template>

<script>
export default {
  name: "LoginPage",
  methods:{
    redirectSignUp() {
      this.$router.push({ name: 'SignUp'})   //use if to redirect under certain conditions

    }
  }
}
</script>

<style scoped>

  router-view{
    display: none;
  }

  .textInput{
    position: relative;
    width: 80%;
    height: 30px;
    display: block;
    align-items: center;
    margin-bottom: 15px;
    left: 8%;
    border-radius: 10px;
    border: 1px solid #919191;
  }

  .submit{
    position: relative;
    display: block;
  }

  .localButton{
    position: relative;
    left: 8%;
  }

  .image{
    position: relative;
    width: 80%;
    left: 8%;
    margin-bottom: 100px;
  }
</style>