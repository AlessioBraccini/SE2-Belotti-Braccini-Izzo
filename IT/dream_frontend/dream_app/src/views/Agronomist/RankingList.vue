<template>
  <div class="square" @click="openBig">

    <h3>Farmers Ranking</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="farmerList.length" style="height: 70%">

      <div class="farmerName">
        <ul>
          <li v-for="farmer in farmerList.length" :key="farmer"> {{ farmerList[farmer-1]['name'] }} </li>
        </ul>
      </div>

      <div class="farmerScore">
        <ul>
          <li v-for="farmer in farmerList.length" :key="farmer"> {{ farmerList[farmer-1]['score'] }} </li>
        </ul>
      </div>

    </div>
    <div v-else class="rawText">No farmers in the ranking</div>
  </div>
</template>

<script>
import {ref} from "vue";
import axios from "axios";
import router from "../../router";
import {serverUrl} from "../../../config";

export default {
  name: "RankingList",

  setup(){

    const farmerList = ref([])
    const error = ref(null)

    // Load the farmers ranking in descending order

    const loadRankData = async () => {
      try {
        await axios.get(serverUrl + '/api/v1/rank_farmers', {params: {ordering: 'descending'}}).then(resp => {
          farmerList.value = resp.data

          if(farmerList.value.length >= 7)
            farmerList.value = farmerList.value.slice(0,7)
        }).catch(err => {
          if (err.response.status === 401){
            localStorage.clear()
            localStorage.setItem('reload', null)
            alert("You lost the connection please log in again");
            router.push({name: 'Login'})
          }
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    if (!farmerList.value.length)
      loadRankData()

    return{ farmerList, error }

  }

}
</script>

<style scoped>

  h3{
    margin: 0;
    padding: 10px 0 0 0;
    height: 10%;
    text-align: center;
  }

  ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  li{
    margin-bottom: 10px;
    border-bottom: solid #919191 1px;
  }

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
    cursor: pointer;
  }

  .rawText{
    position: relative;
    top: 35%;
    left: 23%;
    width: 300px;
  }

  .farmerName{
    position: relative;
    display: inline-block;
    width: 70%;
    left: 7%;
    top: 5%;
    font-weight: bold;

  }

  .farmerScore{
    position: relative;
    display: inline-block;
    width: 16%;
    right: -7%;
    top: 5%;
    text-align: right;
    font-weight: bold;
  }

  @media only screen and (min-width: 700px)  {
    .square{
      width: 90%;
      left: 5%;
      top: 5%;
      height: 380px;
    }
    .rawText{
      left: 37%;
      margin-top: 50px;
      padding-bottom: 50px;
    }
  }

  @media only screen and (min-width: 530px) and (max-width: 699px) {
    .square{
      width: 90%;
      left: 5%;
      top: 5%;
      height: 330px;
    }
  }

</style>