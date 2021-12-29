<template>
  daily el plan
  <button @click="load">dsdsd</button>
</template>

<script>
import axios from "axios";

export default {
  name: "DailyPlan",

  setup(){
    const load = async () => {
      try {

        let axiosConfig = {
          headers:{
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }

        await axios.get('http://localhost:8000/api/v1/users/me', axiosConfig).then(resp => {
          console.log(resp)
        })



      }
      catch (err){
        console.log('err load ' + err)
        // can put the error in the template with the v-if
      }
    }

    return{load}
  }
}
</script>

<style scoped>

</style>