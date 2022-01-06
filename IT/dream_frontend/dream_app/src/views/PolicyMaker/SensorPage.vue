<template>
  <div>
    <HumidityChart/>
    <IrrigationChart/>
  </div>
</template>

<script>
import IrrigationChart from "@/views/PolicyMaker/IrrigationChart";
import HumidityChart from "@/views/PolicyMaker/HumidityChart";

export default {
  name: 'App',
  components: {IrrigationChart, HumidityChart}

  // setup(){
  //
  //   const name = ref(localStorage.getItem('name'))
  //   // const data = null
  //   //
  //   // const loadHumidity = async () => {
  //   //   try {
  //   //     await axios.get('http://localhost:8000/api/v1/rank_farmers',  {params: {ordering: props.ordering, district: ''}}).then(resp => {
  //   //       farmerList.value = resp.data
  //   //
  //   //       if(farmerList.value.length >= 7)
  //   //         farmerList.value = farmerList.value.slice(0,7)
  //   //     })
  //   //   }
  //   //   catch (err){
  //   //     error.value = err.message
  //   //     console.log(err.message)
  //   //   }
  //   // }
  //
  //   return{ name }
  //
  // }
}
</script>

<style scoped>
canvas {
  background: white;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
}
</style>