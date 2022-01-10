<template>
  <NavbarAgro :name="name" />

  <RankingListPM @click="bigRanking" ordering="descending" title="Top Farmers"/>
  <RankingListPM @click="bigRankingAsc" ordering="ascending" title="Worst Farmers"/>

  <button @click="pushSensors" class="actionButton backBtn">View Sensors Data</button>
  <button @click="pushReport" class="actionButton backBtn">View Steering Initiative</button>

</template>

<script>
import NavbarAgro from "@/views/Navbar";
import {ref} from "vue";
import RankingListPM from "@/views/PolicyMaker/RankingListPM";
import router from "@/router";

export default {
  name: "PolicyMakerHomepage",
  components: {RankingListPM, NavbarAgro},

  setup(){
    const name = ref(localStorage.getItem('name'))


    const bigRanking = () => {
      localStorage.setItem('order', 'descending')
      router.push({ name: 'RankingPM' })
    }

    const bigRankingAsc = () => {
      localStorage.setItem('order', 'ascending')
      router.push({ name: 'RankingPM' })
    }

    const pushReport = () => {
      router.push({ name: 'ViewReport' })
    }

    const pushSensors = () => {
      router.push({ name: 'Sensors' })
    }



    return { name, bigRanking, bigRankingAsc, pushReport, pushSensors }

  }
}
</script>

<style scoped>

  .backBtn{
    position: relative;
    width: 90%;
    left: 5%;
  }

</style>