<template style="height: auto">
  <NavbarAgro :name="name" class="agroNav"/>

  <div class="mainBody">
    <div>
      <WeatherAgro :area="area" @click="weatherPage"/>
      <RankingList @click="bigRanking"/>
    </div>
    <div>
      <button class="actionButton localButton" @click="handlePlan">Daily Plan</button>
      <button class="actionButton localButton" @click="handleMessage">Help Requests <span class="notification">{{requests.length}}</span> </button>
      <button class="actionButton localButton" @click="handleReports">Steering Initiative</button>
    </div>
  </div>
</template>

<script>
import NavbarAgro from "@/views/Navbar";
import {ref} from "vue";
import WeatherAgro from "@/views/Agronomist/WeatherAgro";
import RankingList from "@/views/Agronomist/RankingList";
import router from "@/router";
import axios from "axios";
import {serverUrl} from "../../../config";

export default {
  name: "AgronomistHomepage",
  components: {RankingList, WeatherAgro, NavbarAgro},
  setup(){

    const name = ref(localStorage.getItem('name'))
    const area = ref(localStorage.getItem('district'))
    const requests = ref([])

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadRequests =  async () => {
      try {
        await axios.get(serverUrl + '/api/v1/help_request').then(resp => {
          requests.value = resp.data
        }).catch(err => {
          if (err.response.status === 401){
            localStorage.clear()
            localStorage.setItem('reload', null)
            alert("You lost the connection please log in again");
            router.push({name: 'Login'})
          }
        })
      }
      catch(err) {
        console.log(err.toString())
      }
    }

    loadRequests()

    const handleMessage = () => {
      router.push({ name: 'HelpRequests' })
    }

    const handlePlan = () => {
        router.push({ name: 'DailyPlan' })
    }

    const handleReports = () => {
      router.push({ name: 'WriteReport' })
    }

    const bigRanking = () => {
      router.push({ name: 'RankPage' })
    }

    const weatherPage = () => {
      router.push({ name: 'WeatherAgro' })
    }


    // load user data from api

    return{ name, area, requests, handleMessage, handlePlan, handleReports, bigRanking, weatherPage }
  }
}
</script>

<style scoped>
  .agroNav{
    position: relative;
    display: block;
    top: 0;
  }

  .mainBody{
    position: relative;
    height: auto;
  }

  .localButton{
    position: relative;
    width: 90%;
    left: 5%;
  }

  .notification{
    display: inline-block;
    background-color: red;
    border-radius: 50%;
    width: 25px;
  }

  @media only screen and (min-width: 750px) {
    .localButton {
      width: 26.5%;
      margin-right: 5%;
      left: 5%;
      margin-top: 2%;
      margin-bottom: 2%;
    }
  }

</style>