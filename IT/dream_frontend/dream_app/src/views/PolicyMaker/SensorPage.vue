<template>

  <Navbar :name="name"/>

  <div>
    <HumidityChart/>
    <IrrigationChart/>
  </div>
  <button @click="pushRaw" class="actionButton backBtn" style="margin-bottom: 0">Raw Data</button>
  <button @click="back" class="actionButton backBtn1">Back</button>

</template>

<script>
import IrrigationChart from "@/views/PolicyMaker/IrrigationChart";
import HumidityChart from "@/views/PolicyMaker/HumidityChart";
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import router from "@/router";

export default {
  name: 'App',
  components: {Navbar, IrrigationChart, HumidityChart},

  setup(){

    const name = ref(localStorage.getItem('name'))

    const back = () => {
      router.push({name: 'PMHome'})
    }

    const pushRaw = () => {
      router.push({name: 'RawData'})
    }

    return{ name, back, pushRaw }

  }
}
</script>

<style scoped>
  canvas {
    background: white;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
  }

  .backBtn{
    width: 91%;
    left: 4%;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .backBtn1{
    width: 91%;
    left: 4%;
    margin-bottom: 20px;
  }
</style>