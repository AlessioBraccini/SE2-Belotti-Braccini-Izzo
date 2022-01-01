<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <h3>Day of the visits</h3>
    <div>
      <input type="date" v-model="date" class="date"/>
    </div>

    <h3>Farmers</h3>

    <div class="farmerArea">

      <div v-if="error" style="text-align: center">{{ error }}</div>
      <div v-else-if="farmerList.length" style="height: 70%">

        <div class="farmerName">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="addFarmer(farmer-1)"> {{ farmerList[farmer-1]['name'] }} </li>
          </ul>
        </div>

        <div class="farmerScore">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="addFarmer(farmerList[farmer-1])"> {{ farmerList[farmer-1]['score'] }} </li>
          </ul>
        </div>

      </div>
      <div v-else class="rawText">Loading...</div>
    </div>

    <h3>el Plan</h3>

    <div class="takenFarmerArea">
      <div v-if="takenFarmerList.length" style="height: 70%">

        <div class="takenFarmerName">
          <ul>
            <li v-for="farmer in takenFarmerList.length" :key="farmer" @click="removeFarmer(farmerList[farmer-1])"> {{ takenFarmerList[farmer-1]['name'] }} </li>
          </ul>
        </div>
      </div>
      <div v-else class="rawText">No farmer selected</div>
    </div>

    <h3>Annotation</h3>
    <div class="divTextArea">
      <textarea class="textArea" v-model="annotations"/>
    </div>

  </div>

  <button @click="uploadDailyPlan" class="actionButton confirmBtn">Confirm Plan</button>
  <button @click="updateDailyPlan" class="actionButton confirmBtn">Update Today Plan</button>
  <button @click="showDailyPlan" class="actionButton confirmBtn">Show Created Plan</button>
  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import {ref} from "vue";
import axios from "axios";
import NavbarAgro from "@/views/Agronomist/NavbarAgro";
import router from "@/router";


export default {
  name: "DailyPlan",
  components: {NavbarAgro},
  setup(){

    const name = localStorage.getItem('name')
    const farmerList = ref([])
    const takenFarmerList = ref([])
    const date = ref(null)
    const annotations = ref('')
    const error = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const uploadDailyPlan =  () => {
      // try {
      //   await axios.post('http://localhost:8000/api/v1/daily_plan', {
      //
      //     farmer_list: takenFarmerList.value,
      //     annotations: annotations.value
      //
      //   }).then(resp => {
      //       console.log(resp.data)
      //     }).catch(err => {
      //       console.log(err)
      //     })
      // }
      // catch (err){
      //   console.log('err load ' + err)
      //   // can put the error in the template with the v-if
      // }

      localStorage.setItem('dailyPlan', 'true')

      router.push({ name: 'AgroHome' })


    }

    const loadRankData = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/rank_farmers', {params: {ordering: 'descending'}}).then(resp => {
          farmerList.value = resp.data
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    if (!farmerList.value.length)
      loadRankData()

    const addFarmer = (farmer) => {
      takenFarmerList.value.push(farmerList.value[farmer])
      farmerList.value.splice(farmer, 1)
    }

    const removeFarmer = (farmer) => {
      takenFarmerList.value.splice(farmer, 1)
    }

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    const updateDailyPlan = () => {
      router.push({name: 'UpdatePlan'})
    }

    const showDailyPlan = () => {
      router.push({name: 'ShowPlan'})
    }

    return{ name, farmerList, error, takenFarmerList, annotations, date, uploadDailyPlan, addFarmer, removeFarmer, updateDailyPlan, showDailyPlan, back }
  }
}
</script>

<style scoped>

  h3{
    margin: 0;
    padding: 10px 0 0 21px;
    height: 10%;
    left: 5%;
    text-align: left;
  }

  ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  li{
    margin-bottom: 10px;
    border-bottom: solid #919191 1px;
    cursor: pointer;
  }

  li:hover{
    background-color: #004643;
    color: #ffffff;
    border-radius: 5px;
    padding-left: 10px;
  }

  .square{
    position: relative;
    display: block;
    background-color: #E9C197;
    width: 90%;
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
  }

  .date{
    position: relative;
    left: 5%;
    border-radius: 10px;
  }

  .farmerArea{
    position: relative;
    display: block;
    background-color: white;
    width: 90%;
    height: 300px;
    left: 5%;
    border-radius: 22px;
    overflow: scroll;
  }

  .takenFarmerArea{
    position: relative;
    display: block;
    background-color: white;
    width: 90%;
    height: 130px;
    left: 5%;
    border-radius: 22px;
    overflow: scroll;
  }

  .divTextArea{
    position: relative;
    display: block;
    width: 88%;
    height: 125px;
    left: 5%;
  }

  .textArea{
    width: 100%;
    height: 100px;
    left: 5%;
    border-radius: 12px;
    resize: none;
  }

  .rawText{
    position: relative;
    top: 45%;
    left: 24%;
    width: 165px;
  }

  .farmerName{
    position: relative;
    display: inline-block;
    width: 70%;
    left: 7%;
    top: 5%;
    font-weight: bold;
  }

  .takenFarmerName{
    position: relative;
    display: inline-block;
    width: 85%;
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

  .backBtn{
    width: 90%;
    left: 5%;
    margin-bottom: 20px;
  }

  .confirmBtn{
    width: 90%;
    left: 5%;
  }

</style>