<template>
  <Navbar :name="name"/>

  <div class="square">

    <h3>Steering Initiative</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="reportList.length" class="scrollDiv">
      <div>
        <div class="farmerName">
          <ul>
            <li v-for="farmer in reportList.length" :key="farmer" @click="viewSpecificReport(reportList[farmer-1])"> {{ reportList[farmer-1]['name'] }} </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else class="rawText">Loading...</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";

export default {
  name: "ViewReport",
  components: {Navbar},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const reportList = ref([])
    const error = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadReport = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/steering_initiatives').then(resp => {
          console.log(resp.data)
          reportList.value = resp.data
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    loadReport()

    const viewSpecificReport = (farmer) => {

      localStorage.setItem('id', farmer['user_id'])

      router.push({name: 'SpecificInfo'})
    }

    const back = () => {
      router.push({name: 'PMHome'})
    }

    return{ name, reportList, error, back, viewSpecificReport }
  }
}
</script>

<style scoped>
  h3{
    margin: 0;
    padding: 10px 0 0 0;
    height: 5%;
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
    height: 620px;
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
  }

  .district{
    position: relative;
    left: 6%;
    padding-top: 15px;
  }

  .inputDist{
    position: relative;
    width: 69%;
    height: 30px;
    background-color: #E9C197;
    border: solid #919191 2px;
    border-radius: 10px;
    font-size: 15px;
  }

  .rawText{
    position: relative;
    text-align: center;
  }

  .scrollDiv{
    height: 90%;
    max-height: 83%;
    overflow-y: scroll;
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

  .backBtn{
    width: 90%;
    left: 5%;
    margin-top: 20px;
  }

</style>