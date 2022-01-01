<template>
  <header class="App-header">
    <div class="divProfileImg"><img :src="profileimg" class="profileImg" alt="img"/></div>
    <div class="spanText">
      <p class="welcomeMessage"> Welcome, </p>
      <h3 class="usernameStyle">{{ name }}</h3>
    </div>
    <div class="dropdown">
      <button class="menuButton">⋮</button>
      <div class="dropdown-content">
        <router-link :to="{ name: 'AgroHome' }">Home</router-link>
        <a href="#" @click="logout">Logout</a>
      </div>
    </div>
  </header>
</template>

<script>
import profileimg1 from '../assets/profile.png'
import axios from "axios";
import router from "@/router";

export default {
  name: "NavbarAgro",
  props: ['name'],

  setup(){
    const profileimg = profileimg1;

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const logout = () => {

      axios.post('http://localhost:8000/api/v1/token/logout/')
      .then(() => {
        localStorage.clear()

        localStorage.setItem('reload', null)

        router.push({name: 'Login'})

      })


    }
    return{ profileimg, logout }
  }
}
</script>

<style scoped>

  .App-header {
    background-color: #faf4d3;
    height: 60px;
    font-size: calc(10px + 2vmin);
    width: 100%;
    z-index: 1;
    position: relative;
    display: block;
    top: 0;
  }

  .divProfileImg{
    position: relative;
    display: inline-block;
    width: 40px;
    height: 40px;
    left: 5%;
    top: 11px;
  }

  .profileImg{
    width: 40px;
    height: 40px;
    border-radius: 20px;
  }

  .spanText{
    display: inline-block;
    position: relative;
    width: auto;
    left: 10%;
    top: 10px;
  }
  .menuButton{
    display: inline-block;
    position: relative;
    width: 40px;
    height: 40px;
    border-radius: 20px;
    background-color: #004643;
    font-size: 30px;
    color: white;
    left: 0;
  }

  .usernameStyle{
    position: relative;
    color: black;
    margin: 0;
  }






  /* The container <div> - needed to position the dropdown content */
  .dropdown {
    position: relative;
    display: inline-block;
    float: right;
    right: 7%;
    top: 10px;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #faf4d3;
    min-width: 160px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    z-index: 1;
    right: 0;
    border: solid 1px #919191;
    border-radius: 10px;
  }

  .dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }

  /* Change color of dropdown links on hover */
  .dropdown-content a:hover {
    border-radius: 10px;
    background-color: #004643;
    color: #faf4d3;
  }

  /* Show the dropdown menu on hover */
  .dropdown:hover .dropdown-content {display: block;}

</style>