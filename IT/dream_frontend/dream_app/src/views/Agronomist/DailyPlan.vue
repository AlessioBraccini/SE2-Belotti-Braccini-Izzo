<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <h3>Day of the visits</h3>
    <div>
      <input type="date" v-model="date" class="date"/>
      <div v-if="dateErr" class="dateError">{{dateErr}}</div>
    </div>

    <h3>Farmers</h3>

    <div class="farmerArea">

      <div v-if="error" style="text-align: center">{{ error }}</div>
      <div v-else-if="farmerList.length" style="height: 70%">

        <div class="farmerName">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="addFarmer(farmer-1)"> {{ farmerList[farmer-1]['farmer_name'] }} </li>
          </ul>
        </div>

        <div class="farmerScore">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="addFarmer(farmer-1)"> {{ farmerList[farmer-1]['visit_ctr'] }} </li>
          </ul>
        </div>

      </div>
      <div v-else class="rawText">Loading...</div>
    </div>
    <div>
      <h3 style="display: inline-block">Plan</h3>
      <div v-if="listErr" class="listError">{{listErr}}</div>
    </div>

    <div class="takenFarmerArea">
      <div v-if="takenFarmerList.length" style="height: 70%">

        <div class="takenFarmerName">
          <ul>
            <li v-for="farmer in takenFarmerList.length" :key="farmer" @click="removeFarmer(farmerList[farmer-1])"> {{ takenFarmerList[farmer-1]['farmer_name'] }} </li>
          </ul>
        </div>
      </div>
      <div v-else class="rawText">No farmer selected</div>
    </div>

    <div v-if="errorMsg" class="errorMsg">{{ errorMsg }}</div>

    <div style="height: 20px"/>

  </div>

  <button @click="uploadDailyPlan" class="actionButton confirmBtn">Confirm Plan</button>
  <button @click="updateDailyPlan" class="actionButton confirmBtn">Update Today Plan</button>
  <button @click="showDailyPlan" class="actionButton confirmBtn">Show Created Plan</button>
  <button @click="back" class="actionButton backBtn">Back</button>

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
    const takenFarmerList = ref([])
    const takenFarmerListId = ref([])
    const date = ref(null)
    const annotations = ref('')
    const error = ref(null)
    const dateErr = ref('')
    const listErr = ref('')
    const confirmationMessage = ref('')
    const errorMsg = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const uploadDailyPlan =  async () => {
      try {
        dateErr.value = ''
        listErr.value = ''
        errorMsg.value = ''

        if (date.value) {
          if (takenFarmerList.value.length){
            await axios.post('http://localhost:8000/api/v1/daily_plan', {
              visit_farmers_list: takenFarmerListId.value,   // lista di id dei farmers
              date: date.value
            }).then(() => {
              scroll(0,0)
              confirmationMessage.value = 'Plan send successfully'

              setTimeout(function() {
                router.push({name: 'AgroHome'})
              }, 1250);

            }).catch(() => {
              errorMsg.value = 'You have already make a plan for this day'
            })
          }
          else {
            listErr.value = '! List cannot be empty'
          }
        } else {
          if (!takenFarmerList.value.length)
            listErr.value = '! List cannot be empty'
          dateErr.value = "! Date is required"
        }
      }
      catch(err) {
          console.log('err load ' + err)
          // can put the error in the template with the v-if
      }
    }

    const loadFarmerData = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/farms_list').then(resp => {
          farmerList.value = resp.data
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    if (!farmerList.value.length)
      loadFarmerData()

    const addFarmer = (farmer) => {
      if(takenFarmerListId.value.indexOf(farmerList.value[farmer]['farmer_id']) === -1) {
        takenFarmerList.value.push(farmerList.value[farmer])
        takenFarmerListId.value.push(farmerList.value[farmer]['farmer_id'])
      }
    }

    const removeFarmer = (farmer) => {
      takenFarmerList.value.splice(farmer, 1)
      takenFarmerListId.value.splice(farmer, 1)
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

    return{ name, farmerList, error, takenFarmerList, annotations, date, dateErr, listErr, confirmationMessage, errorMsg,uploadDailyPlan, addFarmer, removeFarmer, updateDailyPlan, showDailyPlan, back }
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
    height: 30px;
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

  .takenFarmerArea{
    position: relative;
    display: block;
    background-color: white;
    width: 90%;
    height: 130px;
    left: 5%;
    border-radius: 22px;
    overflow-y: scroll;
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

  .dateError{
    position: relative;
    display: inline-block;
    width: 180px;
    left: 24px;
    color: red;
  }

  .listError{
    position: relative;
    display: inline-block;
    width: 180px;
    left: 10px;
    color: red;
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
  @media only screen and (min-width: 612px) and (max-width: 1700px) {
    .dateError{
      position: relative;
      display: inline-block;
      width: 200px;
      left: 7%;
      color: red;
    }

    .backBtn, .confirmBtn {
      width: 40%;
      margin-right: 10%;
      left: 5%;
      display: inline-block;
    }
  }


</style>