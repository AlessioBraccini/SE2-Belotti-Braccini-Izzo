<template>
  <NavbarAgro :name="name"/>

  <div class="square" @click="openBig">

    <h3>Farmers Ranking</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="farmerList.length" class="scrollDiv">
      <div>
        <div class="farmerName">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="viewSpecificInfo(farmerList[farmer-1])"> {{ farmerList[farmer-1]['name'] }} </li>
          </ul>
        </div>

        <div class="farmerScore">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="viewSpecificInfo(farmerList[farmer-1])"> {{ farmerList[farmer-1]['score'] }} </li>
          </ul>
        </div>
      </div>

    </div>
    <div v-else class="rawText">Loading...</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>



</template>

<script>
import NavbarAgro from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";
export default {
  name: "RankingView",
  components: {NavbarAgro},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const farmerList = ref([])
    const error = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadRankData = async () => {
      try {
        await axios.get('https://appdream.herokuapp.com/api/v1/rank_farmers', {params: {ordering: 'descending'}}).then(resp => {
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

    const viewSpecificInfo = (farmer) => {

      localStorage.setItem('id', farmer['user_id'])

      router.push({name: 'SpecificInfo'})
    }

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    return{ name, farmerList, error, back, viewSpecificInfo }

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
    height: 600px;
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

  .scrollDiv{
    height: 90%;
    max-height: 90%;
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

  @media only screen and (min-width: 600px)  {
    .backBtn{
      margin-bottom: 2%;
    }
  }

</style>