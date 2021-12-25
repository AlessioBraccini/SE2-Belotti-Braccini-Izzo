<template>
  <header class="App-header">
    <div class="divProfileImg"><img src="" class="profileImg" alt="img"/></div>
    <div class="spanText">
      <p class="welcomeMessage"> Welcome, </p>
      <h3 class="usernameStyle">{{ name }}</h3>
    </div>
    <button class="menuButton">⋮</button>

    <div id="nav">
      <router-link :to="{ name: 'AgroHome' }">Home</router-link>
      <router-link :to="{ name: 'About' }">About</router-link>
    </div>
  </header>

</template>

<script>


export default {
  name: "NavbarAgro",
  props: ['name'],

  setup(){

  }
}
</script>

<style scoped>

  .App-header {
    background-color: #faf4d3;
    height: 60px;
    font-size: calc(10px + 2vmin);
    width: 100%;
    position: fixed;
    z-index: 1;
  }

  .divProfileImg{
    position: relative;
    display: inline-block;
    width: 40px;
    height: 40px;
    left: 5%;
    top: 10px;
  }

  .profileImg{
    width: 40px;
    height: 40px;
    border-radius: 20px;
  }

  .spanText{
    display: inline-block;
    position: relative;
    width: 80px;
    left: 10%;
    top: 10px;
  }
  .menuButton{
    display: inline-block;
    position: relative;
    width: 40px;
    height: 40px;
    left: 45%;
    border-radius: 20px;
    background-color: #004643;
    font-size: 30px;
    color: white;
  }

  .usernameStyle{
    position: relative;
    width: 80px;
    color: black;
    margin: 0;
  }

</style>