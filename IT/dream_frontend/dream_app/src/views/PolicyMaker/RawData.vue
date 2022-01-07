<template>
  <Navbar :name="name"/>

  <div class="square">
    <div style="overflow: scroll">
      <h3>Raw data</h3>
      <p class="firstRow">District</p>
      <p class="firstRow">Humidity</p>
      <p class="firstRow">Temperature</p>
      <p class="firstRow">Water Used</p>
      <ul class="ulExt">
        <li>  {{ email }}</li>
        <li>  {{ score }}</li>
        <li>  {{ area }} </li>
        <li>  {{ address }}  </li>
        <ul>
          <li v-for="crop in cropType" :key="crop" class="crop">{{ crop }}</li>
          <li class="last"></li>
        </ul>
      </ul>
    </div>
  </div>
  <button @click="back" class="actionButton backBtn">Back</button>
</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";

export default {
  name: "RawData",
  components: {Navbar},

  setup(){

    const name = localStorage.getItem('name')

    const farmerName = ref('')
    const area = ref('')
    const address = ref('')
    const cropType = ref([])
    const score = ref(0)
    const email = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    axios.get('http://localhost:8000/api/v1/profile_info', {params: {farmer_id: localStorage.getItem('id')}} ).then(resp => {
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
    overflow: scroll;
  }

  li{
    margin: 20px 0 0 0;
    display: inline-block;
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
    overflow: scroll;
  }

  .ulExt{
    position: relative;
    padding-left: 20px;
  }

  .firstRow{
    position: relative;
    display: inline-block;
    left: 3.3%;
    margin-right: 5px;
  }

  .last{
    padding-bottom: 10px;
  }

  .backBtn{
    width: 90%;
    left: 5%;
  }


</style>