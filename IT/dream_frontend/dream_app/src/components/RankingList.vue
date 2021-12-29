<template>
  <div class="square" @click="openBig">
    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="farmerList.length">
      <ul>
<!--        <li v-for="farmer in farmerList" :key="farmerList.name"> {{ farmer }} </li>-->
      </ul>
    </div>
    <div v-else class="rawText">Loading...</div>
  </div>
</template>

<script>
import {ref} from "vue";
import axios from "axios";

export default {
  name: "RankingList",

  setup(){

    const farmerList = ref([])
    const error = ref(null)

    const loadRankData = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/rank_farmers').then(resp => {
          console.log(resp)
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    if (farmerList.value.length)
      loadRankData()

    return{ farmerList, error }

  }

}
</script>

<style scoped>
  .square{
    position: relative;
    display: block;
    background-color: #E9C197;
    width: 90%;
    height: 290px;
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
  }

  .rawText{
    position: relative;
    top: 45%;
    left: 39%;
    width: 100px;
  }
</style>