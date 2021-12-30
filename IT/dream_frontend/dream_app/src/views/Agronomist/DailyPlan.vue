<template>
  <NavbarAgro :name="name"/>
  <div class="container">
    daily el plan
    <button @click="load">dsdsd</button>
  </div>
</template>

<script>
import axios from "axios";
import NavbarAgro from "@/components/NavbarAgro";

export default {
  name: "DailyPlan",
  components: {NavbarAgro},
  setup(){

    const name = localStorage.getItem('name')

    const load = async () => {
      try {

        // {params: {ordering: 'descending', district: 'name of the selected district'}}) for the policy maker
        await axios.get('http://localhost:8000/api/v1/profile_info', {params: {farmer_id: 24}} ).then(resp => {
          console.log(resp.data)
        }).catch(() => {
          console.log('s')
        })
        // await axios.get('http://localhost:8000/api/v1/users/me').then(resp => {console.log(resp)})



      }
      catch (err){
        console.log('err load ' + err)
        // can put the error in the template with the v-if
      }
    }

    return{ name, load }
  }
}
</script>

<style scoped>

  .container{
    position: relative;
  }

</style>