<template>

  <img :src="logo" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">

    <input type="text" required v-model="email" placeholder="Email" class="textInput">

    <input type="password" required v-model="password" placeholder="Password" class="textInput">

    <div v-if="passwordError" class="error">
      {{ passwordError }}
    </div>

    <div class="submit">
      <button class="actionButton localButton">Log In</button>
    </div>
  </form>
  <button class="actionButton localButton" @click="redirectSignUp">Sign Up</button>
</template>

<script>
import { ref } from "vue";
import router from "@/router"
import axios from "axios";
import image from '../assets/dreamLogo.png'
import {serverUrl} from "../config";

export default {
  name: "LoginPage",

  setup(){
    const email = ref('');
    const password = ref('');
    const passwordError = ref('');
    const logo = image;

    if (localStorage.key(0) === 'reload') {
      localStorage.clear()
      location.reload()
    }

    // Retrieve the information of the user in order to load the right homepage
    const loadUserData = async () => {
      try {
        return await axios.get(serverUrl + '/api/v1/users/me/')
      }
      catch (err){
        console.log('err load ' + err)
        // can put the error in the template with the v-if
      }
    }

    // Post in the server the credential, return if they are correct o not
    const handleSubmit = async () => {

      passwordError.value = ''

      await axios.post(serverUrl + '/api/v1/token/login/', {
        email: email.value,
        password: password.value,
      })
          .then(async resp => {

            localStorage.setItem('token', resp.data.auth_token)

            axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

            // Load the correct homepage
            let data = await loadUserData()
            let role = data.data['job_role']
            localStorage.setItem('name', data.data['first_name'] + ' ' + data.data['last_name'] )

            if (data.data['district'] != null)
              localStorage.setItem('district', data.data['district'])

            if (role === 'A') {
              localStorage.setItem('role', 'A')
              router.push({name: 'AgroHome'})
            }
            else if (role === 'P') {
              localStorage.setItem('role', 'P')
              router.push({name: 'PMHome'})
            }
            else {
              localStorage.setItem('role', 'F')
              router.push({name: 'FarmerHome'})
            }

          })
          .catch(err => {
            console.log('error' + err)
            if (err.response.status === 400)
              passwordError.value = 'Email or Password is incorrect'
          }
          )

    }

    const redirectSignUp = () => {
      router.push({ name: 'SignUp'})   //use if to redirect under certain conditions

    }

    return { logo, email, password, passwordError, handleSubmit, redirectSignUp }
  }
}
</script>

<style scoped>

  router-view{
    display: none;
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
    left: 8%;
    margin-bottom: 100px;
    margin-top: 150px;
  }

  .error{
    position: relative;
    width: 80%;
    left: 8%;
    font-size: 20px;
    text-align: center;
    margin: 10px 0 10px 0;
    color: red;
  }

  /*VIEWPORT Responsive */

  @media only screen and (min-width: 600px) {
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
      margin-bottom: 100px;
      margin-top: 100px;
    }

    .error{
      left: 30%;
      width: 48%;
    }
  }

</style>