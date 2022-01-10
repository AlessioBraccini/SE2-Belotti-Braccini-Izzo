<template>
  <Navbar :name="name"/>

  <div class="square">
    <div style="overflow: scroll">
      <h3>Raw data</h3>
      <p class="firstRow">Data are ordered by district in alphabetical order</p>
      <ul class="ulExt">
        <li> Humidity: <br> {{ hum }}</li>
        <li> Temperature: <br> {{ temp }}</li>
        <li> Water quantity: <br> {{ irr }} </li>
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

    const hum = ref(null)
    const temp = ref(null)
    const irr = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    axios.get('http://localhost:8000/api/v1/humidity' ).then(resp => {
      hum.value = resp.data.humidity
      temp.value = resp.data.temperature
    }).catch(err => {
      console.log(err)
    })

    axios.get('http://localhost:8000/api/v1/water_irrigation' ).then(resp => {
      irr.value = resp.data.water_qty
    }).catch(err => {
      console.log(err)
    })

    const back = () => {
      router.go(-1)
    }

    return{ name, hum, temp, irr, back }

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
    padding-left: 13px;
  }

  .firstRow{
    position: relative;
    left: 3.3%;
    margin-right: 5px;
    width: 90%;
  }

  .backBtn{
    width: 90%;
    left: 5%;
  }


</style>