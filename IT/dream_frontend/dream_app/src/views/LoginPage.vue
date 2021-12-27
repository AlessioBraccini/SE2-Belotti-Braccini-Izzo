<template>

  <img :src="logo" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">

    <input type="text" required v-model="email" placeholder="Email" class="textInput">

    <input type="password" required v-model="password" placeholder="Password" class="textInput">

    <div class="submit">
      <button class="actionButton localButton">Log In</button>
    </div>
  </form>
  <button class="actionButton localButton" @click="redirectSignUp">Sign Up</button>
</template>

<script>
import {ref} from "vue";
import router from "@/router"
import axios from "axios";
import image from '../assets/dreamLogo.png'

export default {
  name: "LoginPage",

  setup(){

    const email = ref('');
    const password = ref('');
    const logo = image;
/*
     const load = async () => {
       try {
         let data = await fetch('url dell\' api del server backend')    // serve per trovare la home per l'user
         if (!data.ok) {
           throw Error('error data fetching user')
         }

         // farmerList.value = await data   retrieve data from data
         // use these data
       }
       catch (err){
         error.value = err.message
         // can put the error in the template with the v-if
       }
     }
     */

    const handleSubmit = () => {
      axios.post('http://127.0.0.1:8000/api/v1/token/login/', {
        email: email.value,
        password: password.value,
      })
          .then(resp => {
            console.log(resp + 'risposta')
            // let data = load()
            //
            // if (user === agronomist)
            //   router.push(name: 'AgronomistHome')
            // else if (user === PM)
            //   router.push(name: 'PolicyMakerHome')

          })
          .catch(err =>  console.log('error' + err))
    }

    const handleSubmittemp = () => {

      if (email.value === 'agro')
        router.push({name: 'AgroHome'})
      else
        router.push({name: 'PMHome'})

    }

    const redirectSignUp = () => {
      router.push({ name: 'SignUp'})   //use if to redirect under certain conditions

    }

    return { logo, email, password, handleSubmit, redirectSignUp, handleSubmittemp }
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
</style>