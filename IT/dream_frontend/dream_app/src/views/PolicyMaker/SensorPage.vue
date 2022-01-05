<template>
  <Navbar :name="name"/>

  <div class="square">

  </div>

</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";

export default {
  name: "SensorPage",
  components: {Navbar},

  setup(){

    const name = ref(localStorage.getItem('name'))
    // const data = null
    //
    // const loadHumidity = async () => {
    //   try {
    //     await axios.get('http://localhost:8000/api/v1/rank_farmers',  {params: {ordering: props.ordering, district: ''}}).then(resp => {
    //       farmerList.value = resp.data
    //
    //       if(farmerList.value.length >= 7)
    //         farmerList.value = farmerList.value.slice(0,7)
    //     })
    //   }
    //   catch (err){
    //     error.value = err.message
    //     console.log(err.message)
    //   }
    // }

    return{ name }
  }
}
</script>

<style scoped>

</style>