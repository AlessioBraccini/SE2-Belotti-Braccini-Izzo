<template style="height: auto">
  <NavbarAgro :name="name" class="agroNav"/>

  <div class="mainBody">
    <div>
      <WeatherAgro :area="area" @click="weatherPage"/>
      <RankingList @click="bigRanking"/>
    </div>
    <div>
      <button class="actionButton localButton" @click="handlePlan">Daily Plan</button>
      <button class="actionButton localButton" @click="handleMessage">Help Requests</button>
      <button class="actionButton localButton" @click="handleReports">Send Report</button>
    </div>
  </div>
</template>

<script>
import NavbarAgro from "@/components/NavbarAgro";
import {ref} from "vue";
import WeatherAgro from "@/components/WeatherAgro";
import RankingList from "@/components/RankingList";
import router from "@/router";

export default {
  name: "AgronomistHomepage",
  components: {RankingList, WeatherAgro, NavbarAgro},
  setup(){

    const name = ref(localStorage.getItem('name'))
    const area = ref(localStorage.getItem('district'))

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

    return{ name, area, handleMessage, handlePlan, handleReports, bigRanking, weatherPage }
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
</style>