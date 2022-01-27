<template>
  <NavbarAgro :name="name"/>

  <div class="square">
    <h3>Specific farmer info</h3>
    <ul>
      <li v-for="farmer in farmerList.length" :key="farmer"> {{ farmerList[farmer-1]['farmer_name'] }} </li>
    </ul>
  </div>
  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import NavbarAgro from "@/views/Navbar";
import axios from "axios";
import {ref} from "vue";
import router from "@/router";
import {serverUrl} from "../../config";

export default {
  name: "ViewSpecificPlan",
  components: {NavbarAgro},
  props:['id'],

  setup(){

    const name = localStorage.getItem('name')
    const date = localStorage.getItem('id')

    const farmerList = ref([])
    const errorMsg = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    // Load the specific plan by using date as a parameter
    const loadDailyPlan = async () => {
      console.log(date)
      await axios.get(serverUrl + '/api/v1/update_daily_plan', {params: {date: date}})
          .then(resp => {
            farmerList.value = resp.data['visit_farmers_list']
          }).catch(err => {
            console.log(err)
            errorMsg.value = 'No plan for today'
            if (err.response.status === 401){
              localStorage.clear()
              localStorage.setItem('reload', null)
              alert("You lost the connection please log in again");
              router.push({name: 'Login'})
            }
          })
    }

    loadDailyPlan()

    const back = () => {
      router.go(-1)
    }

    return{ name, farmerList, back }

  }
}
</script>

<style scoped>

ul{
  padding-bottom: 20px;
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

.backBtn{
  width: 90%;
  left: 5%;

}

</style>