<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <h3>Farmers of the day</h3>

    <div class="farmerArea">

      <div v-if="error" style="text-align: center">{{ error }}</div>
      <div v-else-if="farmerList.length" style="height: 70%">

        <div class="dailyPlan">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="removeFarmer(farmer-1)"> {{ farmerList[farmer-1]['farmer_name'] }} </li>
          </ul>
        </div>
      </div>
      <div v-else class="rawText">No farmer in the plan</div>
    </div>

    <div v-if="errorMsg" class="errorMsg">{{ errorMsg }}</div>

    <h3>Complete farmers list</h3>

    <div class="farmerArea">

      <div v-if="error" style="text-align: center">{{ error }}</div>
      <div v-else-if="completeFarmerList.length" style="height: 70%">

        <div class="farmerName">
          <ul>
            <li v-for="farmer in completeFarmerList.length" :key="farmer" @click="addFarmer(farmer-1)"> {{ completeFarmerList[farmer-1]['farmer_name'] }} </li>
          </ul>
        </div>

        <div class="farmerScore">
          <ul>
            <li v-for="farmer in completeFarmerList.length" :key="farmer" @click="addFarmer(farmer-1)"> {{ completeFarmerList[farmer-1]['visit_ctr'] }} </li>
          </ul>
        </div>

      </div>
      <div v-else class="rawText">Loading...</div>
    </div>

    <div style="height: 20px"/>

  </div>

  <button @click="confirmUpdate" class="actionButton backBtn">Confirm Update</button>
  <button @click="back" class="actionButton backBtn" style="margin-bottom: 20px;">Back</button>

  <div v-if="confirmationMessage" class="opacityBack">
    <div  class="confirmMsg">
      <h4 class="confirmText"> {{ confirmationMessage }} </h4>
    </div>
  </div>

</template>

<script>
import {ref} from "vue";
import axios from "axios";
import NavbarAgro from "@/views/Navbar";
import router from "@/router";


export default {
  name: "DailyPlan",
  components: {NavbarAgro},
  setup(){

    const name = localStorage.getItem('name')
    const farmerList = ref([])
    // const date = new Date().toJSON().slice(0,10)
    const date = '2022-01-07'
    const annotations = ref('')
    const error = ref(null)
    const dateErr = ref('')
    const listErr = ref('')
    const confirmationMessage = ref('')
    const errorMsg = ref('')

    const completeFarmerList = ref([])
    const farmerListId = ref([])

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadDailyPlan = async () => {
      await axios.get('http://localhost:8000/api/v1/daily_plan', {params: {date: date}})
          .then(resp => {
            farmerList.value = resp.data['visit_farmers_list']

            for (let i = 0; i < farmerList.value.length; i++)
              farmerListId.value.push(farmerList.value[i]['farmer_id'])
          }).catch(err => {
            console.log(err)
            errorMsg.value = 'No plan for today'
          })
    }

    const loadFarmerData = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/farms_list').then(resp => {
          completeFarmerList.value = resp.data
          loadDailyPlan()
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    loadFarmerData()

    const addFarmer = (farmer) => {
      if(farmerListId.value.indexOf(completeFarmerList.value[farmer]['farmer_id']) === -1) {
        farmerList.value.push(completeFarmerList.value[farmer])
        farmerListId.value.push(completeFarmerList.value[farmer]['farmer_id'])
      }
    }

    const removeFarmer = (farmer) => {
      farmerList.value.splice(farmer, 1)
      farmerListId.value.splice(farmer, 1)
    }

    const back = () => {
      router.go(-1)
    }

    const confirmUpdate = async () => {
        await axios.post ('http://localhost:8000/api/v1/update_daily_plan', {
          visit_farmers_list: farmerListId.value,
          date: date
        }).then(() => {
          scroll(0,0)
          confirmationMessage.value = 'Plan Update Successfully'

          setTimeout(function() {
            router.push({name: 'AgroHome'})
          }, 1250);


        }).catch(() => {

        })

    }

    return{ name, farmerList, error, completeFarmerList, annotations, date, dateErr, listErr, confirmationMessage, errorMsg, confirmUpdate, addFarmer, removeFarmer, back }
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

.farmerArea{
  position: relative;
  display: block;
  background-color: white;
  width: 90%;
  height: 300px;
  left: 5%;
  border-radius: 22px;
  overflow-y: scroll;
}

.rawText{
  position: relative;
  top: 45%;
  left: 23%;
  width: 180px;
}

.farmerName{
  position: relative;
  display: inline-block;
  width: 70%;
  left: 7%;
  top: 5%;
  font-weight: bold;
}

.dailyPlan{
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
}

.confirmMsg{
  position: absolute;
  z-index: 999;
  width: 80%;
  height: 100px;
  background-color: #E9C197;
  text-align: center;
  border: #919191 2px solid;
  border-radius: 10px;
  left: 8%;
  top: 40%;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  color: black;
}

.confirmText{
  position: relative;
  top: 35px;
  margin: 0;
}

.opacityBack{
  z-index: 99;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(40, 70, 70, 0.8);
  top: 0;
  display: block;
}

.errorMsg{
  position: relative;
  color: red;
  left: 5%;
}

</style>