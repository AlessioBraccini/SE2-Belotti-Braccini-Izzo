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
import {ref} from "vue";
import router from "@/router"
import axios from "axios";
import image from '../assets/dreamLogo.png'

export default {
  name: "LoginPage",

  setup(){

    const email = ref('ale@b.it');
    const password = ref('ale99magic');
    const passwordError = ref('');
    const logo = image;

    const load = async () => {
      try {
        let data = await fetch('http://localhost:8000/api/v1/account_type/')
        // let data = await fetch('http://localhost:8000/api/v1/users/me/')    // va ma da errore tipo 'credentials not provided'

        if (!data.ok) {
           throw Error('error data fetching user')
        }
        console.log('load ' + data)

        // farmerList.value = await data   retrieve data from data
        // use these data
      }
      catch (err){
        console.log('err load ' + err)
        // can put the error in the template with the v-if
      }
    }


    const handleSubmit = async () => {

      passwordError.value = ''

      await axios.post('http://localhost:8000/api/v1/token/login/', {
        email: email.value,
        password: password.value,
      })
          .then(async resp => {
            console.log(resp + ' risposta')

            let data = await load()
            console.log('fine load ' + data)

            //
            // if (user === agronomist)
            //   router.push(name: 'AgronomistHome')
            // else if (user === PM)
            //   router.push(name: 'PolicyMakerHome')

            // router.push({name: 'AgroHome'})

          })
          .catch(err => {
            console.log('error' + err)
            if (err.response.status === 400)
              passwordError.value = 'Email or Password is incorrect'
            load(err)
          }
          )

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

    return { logo, email, password, passwordError, handleSubmit, redirectSignUp, handleSubmittemp }
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

</style>