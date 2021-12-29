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


        await axios.get('http://localhost:8000/api/v1/rank_farmers?ordering=descending').then(resp => {
          console.log(resp.data.valueOf())
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