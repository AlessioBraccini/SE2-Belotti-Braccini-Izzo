<template>
  <NavbarAgro :name="name"/>

  <div class="square">
    <h3>Specific farmer info</h3>
    <ul class="ulExt">
      <li> <b>Farmer name</b>: {{ farmerName }}</li>
      <li> <b>Email</b>: {{ email }}</li>
      <li> <b>Score</b>: {{ score }}</li>
      <li> <b>District</b>: <a :href="'https://www.google.com/maps/search/?api=1&query='+ area" target="_blank"> {{ area }} </a> </li>
      <li> <b>Address</b>: <a :href="'https://www.google.com/maps/search/?api=1&query='+ address" target="_blank"> {{ address }} </a> </li>
      <li> <b>Crop type:</b> </li>
      <ul>
        <li v-for="crop in cropType" :key="crop" class="crop">{{ crop }}</li>
        <li class="last"></li>
      </ul>
    </ul>
  </div>
  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import NavbarAgro from "@/views/Navbar";
import axios from "axios";
import {ref} from "vue";
import router from "@/router";
export default {
  name: "SpecificInfo",
  components: {NavbarAgro},
  props:['id'],

  setup(){

    const name = localStorage.getItem('name')

    const farmerName = ref('')
    const area = ref('')
    const address = ref('')
    const cropType = ref([])
    const score = ref(0)
    const email = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    // Retrieve the info of the farmer in order to display them to the user
    axios.get('https://appdream.herokuapp.com/api/v1/profile_info', {params: {farmer_id: localStorage.getItem('id')}} ).then(resp => {
      farmerName.value = resp.data['full_name']
      email.value = resp.data['email']
      area.value = resp.data['area']
      score.value = resp.data['score']
      address.value = resp.data['address']

      for (let i = 0; i < resp.data['crop_types'].length; i++) {
        cropType.value.push(resp.data['crop_types'][i]['crop_type'])
      }

    }).catch(err => {
      console.log(err)
      if (err.response.status === 401){
        localStorage.clear()
        localStorage.setItem('reload', null)
        alert("You lost the connection please log in again");
        router.push({name: 'Login'})
      }
    })

    const back = () => {
      router.go(-1)
    }

    return{ name, farmerName, area, address, cropType, score, email, back }

  }
}
</script>

<style scoped>

  ul{
    list-style-type: none;
  }

  li{
    margin: 20px 0 0 0;
  }

  h3{
    margin: 0;
    padding: 10px 0 0 10px;
    height: 5%;
    text-align: left;
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

  .ulExt{
    position: relative;
    padding-left: 20px;
  }

  .crop{
    list-style-type: decimal;
  }

  .last{
    padding-bottom: 10px;
  }

  .backBtn{
    width: 90%;
    left: 5%;

  }

</style>