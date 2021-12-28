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

        let axiosConfig = {
          headers:{
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }

        return await axios.get('http://localhost:8000/api/v1/users/me', axiosConfig)

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

            localStorage.setItem('token', resp.data.auth_token)

            let data = await load()
            let role = data.data['job_role']
            localStorage.setItem('name', data.data['first_name'] + ' ' + data.data['last_name'] )

            if (role === 'A')
              router.push({name: 'AgroHome'})
            else if (role === 'P')
              router.push({name: 'PMHome'})


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