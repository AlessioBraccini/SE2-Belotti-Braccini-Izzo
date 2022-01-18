<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <div class="district">District:
      <select v-model="district" class="inputDist" @change="changeDistrict">
        <option> All </option>
        <option  v-for="dist in districts" :key="dist"> {{ dist }}</option>
      </select>
    </div>

    <h3>Farmers Ranking</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="farmerList.length" class="scrollDiv">
      <div>
        <div class="farmerName">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="viewSpecificInfo(farmerList[farmer-1])"> {{ farmerList[farmer-1]['name'] }} </li>
          </ul>
        </div>

        <div class="farmerScore">
          <ul>
            <li v-for="farmer in farmerList.length" :key="farmer" @click="viewSpecificInfo(farmerList[farmer-1])"> {{ farmerList[farmer-1]['score'] }} </li>
          </ul>
        </div>
      </div>

    </div>
    <div v-else class="rawText">No farmers in this district</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>



</template>

<script>
import NavbarAgro from "../../views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "../../router";

export default {
  name: "RankingViewPM",
  components: {NavbarAgro},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const farmerList = ref([])
    const error = ref(null)
    const district = ref('All')
    const districts = [
      'Adilabad',
      'Bhadradri Kothagudem',
      'Hanumakonda',
      'Hyderabad',
      'Jagtial',
      'Jangaon',
      'Jayashankar Bhupalpally',
      'Jogulamba Gadwal',
      'Kamareddy',
      'Karimnagar',
      'Khammam',
      'Kumuram Bheem',
      'Mahabubabad',
      'Mahabubnagar',
      'Mancherial',
      'Medak',
      'Medchal-Malkajgiri',
      'Mulugu',
      'Nagarkurnool',
      'Nalgonda',
      'Narayanpet',
      'Nirmal',
      'Nizamabad',
      'Peddapalli',
      'Rajanna Sircilla',
      'Rangareddy',
      'Sangareddy',
      'Siddipet',
      'Suryapet',
      'Vikarabad',
      'Wanaparthy',
      'Warangal',
      'Yadadri Bhuvanagiri',
    ];

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    // Load the farmers ranking by passing a specific ordering and a specific district
    const loadRankData = async () => {
      console.log(district.value)
      try {
        if (district.value === 'All')
          district.value = ''

        await axios.get('https://appdream.herokuapp.com/api/v1/rank_farmers', {params: {ordering: localStorage.getItem('order'), district: district.value}}).then(resp => {
          farmerList.value = resp.data
          if (district.value === '')
            district.value = 'All'
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    if (!farmerList.value.length)
      loadRankData()

    // Redirect to the specific info of a user by using its id
    const viewSpecificInfo = (farmer) => {

      localStorage.setItem('id', farmer['user_id'])

      router.push({name: 'SpecificInfo'})
    }

    // Refresh the ranking if the district is changed
    const changeDistrict = () => {
      loadRankData()
    }

    const back = () => {
      router.push({name: 'PMHome'})
    }

    return{ name, farmerList, error, district, districts, changeDistrict, back, viewSpecificInfo }

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

.district{
  position: relative;
  left: 6%;
  padding-top: 15px;
}

.inputDist{
  position: relative;
  width: 69%;
  height: 30px;
  background-color: #E9C197;
  border: solid #919191 2px;
  border-radius: 10px;
  font-size: 15px;
}

.rawText{
  position: relative;
  text-align: center;
  margin-top: 50px;
}

.scrollDiv{
  height: 90%;
  max-height: 83%;
  overflow-y: scroll;
}

.farmerName{
  position: relative;
  display: inline-block;
  width: 70%;
  left: 7%;
  top: 5%;
  font-weight: bold;

}

.farmerScore{
  position: relative;
  display: inline-block;
  width: 16%;
  right: -7%;
  top: 5%;
  text-align: right;
  font-weight: bold;
}

.backBtn{
  width: 90%;
  left: 5%;
  margin-top: 20px;
}

@media only screen and (min-width: 620px) {

  .backBtn {
    margin-bottom: 2%;
  }
}

</style>