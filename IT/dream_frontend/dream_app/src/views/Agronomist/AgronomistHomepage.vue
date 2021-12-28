<template style="height: auto">
  <NavbarAgro :name="name" class="agroNav"/>

  <div class="mainBody">
    <div>
      <WeatherAgro :area="area"/>
      <RankingList/>
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

    const name = ref('Karun Patel')
    const area = ref('Medak')

    const handleMessage = () => {
      router.push({ name: 'HelpRequests' })
    }

    const handlePlan = () => {
      router.push({ name: 'DailyPlan' })
    }

    const handleReports = () => {
      router.push({ name: 'WriteReport' })
    }


    // load user data from api

    return{ name, area, handleMessage, handlePlan, handleReports }
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