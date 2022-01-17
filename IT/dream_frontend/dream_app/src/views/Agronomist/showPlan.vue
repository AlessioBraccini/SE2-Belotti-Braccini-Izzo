<template>
  <Navbar :name="name"/>

  <div class="square">

    <h3>Steering Initiative</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="planList.length" class="scrollDiv">
      <div>
        <div class="farmerName">
          <ul>
            <li v-for="report in planList.length" :key="report" @click="viewSpecificReport(planList[report-1]['date'])">
              <div> <b> {{ planList[report-1]['date'] }} </b> </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else class="rawText">Loading...</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";

export default {
  name: "ShowPlan",
  components: {Navbar},

  setup(){

    const name = localStorage.getItem('name')
    const planList = ref([])
    const errorMsg = ref('')
    const error = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadPlans = async () => {
      await axios.get('https://appdream.herokuapp.com/api/v1/daily_plan')
          .then(resp => {
            planList.value = resp.data
          }).catch(err => {
            console.log(err)
            errorMsg.value = 'No plan for today'
            error.value = 'no plan'
          })
    }

    loadPlans()

    const viewSpecificReport = (plan) => {

      localStorage.setItem('id', plan.toString())

      router.push({name: 'ViewSpecPlan'})
    }

    const back = () => {
      router.go(-1)
    }

    return{ name, planList, error, errorMsg, back, viewSpecificReport }
  }
}
</script>

<style scoped>
h3{
  margin: 0;
  padding: 10px 0 0 0;
  height: 5%;
  text-align: center;
}

ul{
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li{
  margin-bottom: 10px;
  border-bottom: solid #919191 1px;
  cursor: pointer;
}

li:hover{
  background-color: #004643;
  color: #ffffff;
  border-radius: 5px;
  padding-left: 10px;
}

.square{
  position: relative;
  display: block;
  background-color: #E9C197;
  width: 90%;
  height: 620px;
  left: 5%;
  top: 5%;
  border-radius: 22px;
  margin-top: 20px;
}

.rawText{
  position: relative;
  text-align: center;
}

.scrollDiv{
  height: 90%;
  overflow-y: scroll;
}

.farmerName{
  position: relative;
  display: inline-block;
  width: 86%;
  left: 7%;
  top: 5%;
  font-weight: bold;

}

.backBtn{
  width: 90%;
  left: 5%;
  margin-top: 20px;
}

@media only screen and (min-width: 612px)  {

  .backBtn {

    margin-bottom: 2%;
  }
}

</style>