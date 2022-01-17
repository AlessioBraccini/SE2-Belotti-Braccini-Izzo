<template>
  <img :src="logo" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">
    <input type="text" required v-model="firstName" placeholder="First Name" class="textInput">

    <input type="text" required v-model="lastName" placeholder="Last Name" class="textInput">

    <input type="email" required v-model="email" placeholder="Email" class="textInput">
    <div v-if="userError" class="error">
      {{ userError }}
    </div>

    <div v-if="confirmationMessage" class="opacityBack">
      <div  class="confirmMsg">
        <h4 class="confirmText"> {{ confirmationMessage }} </h4>
      </div>
    </div>

    <input type="password" required v-model="password" placeholder="Password" class="textInput">
    <div v-if="passwordError" class="error">
      {{ passwordError }}
    </div>

    <select v-model="job_role">
      <option value="policyMaker">Policy Maker</option>
      <option value="agronomist">Agronomist</option>
      <option value="farmer">Farmer</option>
    </select>

    <select v-model="selectedDistrict" v-if="job_role!=='policyMaker'">
      <option  v-for="district in district" :key="district"> {{ district }}</option>
    </select>

    <div class="submit">
      <button class="actionButton localButton">Confirm</button>
    </div>
  </form>

  <button class="actionButton localButton" @click="returnLogin">Back</button>

</template>

<script>
import {ref} from "vue";
import axios from "axios";
import router from "@/router";
import image from '../assets/dreamLogo.png'

export default {
  name: "LoginForm",

  setup(){

    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const password = ref('');
    const job_role = ref('policyMaker');
    const passwordError = ref('');
    const userError = ref('');
    const confirmationMessage = ref('');
    const selectedDistrict = ref('Adilabad')
    const district = [
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
    const logo = image;

    const handleSubmit = () => {

      userError.value = ''

      if (password.value.length > 8) {
        passwordError.value = ''

          if (job_role.value === 'policyMaker')
            job_role.value = 'P'
          else if(job_role.value === 'agronomist')
            job_role.value = 'A'
          else
            job_role.value = 'F'

          sendServer()

        } else

          passwordError.value = 'Password must be at least 8 characters long'

    }

    const sendServer = async () => {

      await axios.post('https://appdream.herokuapp.com/api/v1/users/', {
        email: email.value,
        password: password.value,
        first_name: firstName.value,
        last_name: lastName.value,
        job_role: job_role.value,
        district: selectedDistrict.value,
      })
      .then(resp => {
        console.log(resp.data)

        confirmationMessage.value = 'Account created, please log in'

        setTimeout(function() {
          returnLogin()
        }, 1250);

      })
      .catch(err => {
        console.log('error ' + err)
        if (err.response.data.email)
          userError.value = 'Username already exist'
        else if (err.response.data.password) {
          userError.value = 'Password is too similar to email or name'
          job_role.value = 'policyMaker'
        }
        else {
          userError.value = 'Unspecified error'
          job_role.value = 'policyMaker'
        }
      })

  }

    const returnLogin = () => {

      confirmationMessage.value = ''
      router.push({ name: 'Login' })
    }

    return{ logo, firstName, lastName, email, password, job_role, district, passwordError, userError, selectedDistrict, confirmationMessage, handleSubmit, returnLogin }
  }
}
</script>

<style scoped>

  select{
    position: relative;
    width: 81%;
    height: 40px;
    display: block;
    align-items: center;
    margin-bottom: 10px;
    left: 8%;
    background-color: #faf4d3;
    border: solid #919191 2px;
    border-radius: 10px;
    font-size: 15px;
  }

  .textInput{
    position: relative;
    width: 80%;
    height: 30px;
    display: block;
    align-items: center;
    margin-bottom: 15px;
    left: 8%;
    border-radius: 10px;
    border: 1px solid #919191;
  }

  .submit{
    position: relative;
    display: block;
  }

  .localButton{
    position: relative;
    left: 8%;
  }

  .image{
    position: relative;
    width: 80%;
    left: 10%;
    margin-bottom: 100px;
    margin-top: 50px;
  }

  .error{
    position: relative;
    width: 80%;
    left: 8%;
    font-size: 14px;
    margin: -10px 0 10px 0;
  }

  .confirmMsg{
    position: absolute;
    z-index: 999;
    width: 80%;
    height: 100px;
    background-color: #E9C197;
    text-align: center;
    border: #919191 2px solid;
    border-radius: 10px;
    left: 8%;
    top: 40%;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  ;

  }

  .confirmText{
    position: relative;
    top: 35px;
    margin: 0;
    color: black;
  }

  .opacityBack{
    z-index: 99;
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: rgba(40, 70, 70, 0.8);
    top: 0;
    display: block;
  }

  @media only screen and (min-width: 600px){

    select{
      position: relative;
      width: 40%;
      left: 33%;
    }
    .textInput{
      width: 40%;
      height: 30px;
      align-items: center;
      margin-bottom: 15px;
      left: 33%;
    }

    .localButton{
      width: 40%;
      left: 33%;
    }

    .image{
      width: 40%;
      left: 32%;
      margin-bottom: 70px;
      margin-top: 50px;
    }

    .error{
      width: 80%;
      left: 8%;
      font-size: 20px;
      text-align: center;
      margin: 10px 0 10px 0;
    }
  }


</style>