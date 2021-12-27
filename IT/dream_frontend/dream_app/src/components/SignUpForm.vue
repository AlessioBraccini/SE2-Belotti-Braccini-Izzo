<template>
  <img :src="logo" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">
    <input type="text" required v-model="firstName" placeholder="First Name" class="textInput">

    <input type="text" required v-model="lastName" placeholder="Last Name" class="textInput">

    <!-- TODO: make this type email -->
    <input type="text" required v-model="email" placeholder="Email" class="textInput">

    <input type="password" required v-model="password" placeholder="Password" class="textInput">
    <div v-if="passwordError" class="error">
      {{ passwordError }}
    </div>

    <select v-model="role">
      <option value="policyMaker">Policy Maker</option>
      <option value="agronomist">Agronomist</option>
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
import toast from "vue-toast-notification"
import image from '../assets/dreamLogo.png'

export default {
  name: "LoginForm",

  setup(){

    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const password = ref('');
    const role = ref('policyMaker');
    const passwordError = ref('');
    const logo = image;

    const handleSubmit = () => {

      // passwordError.value = password.value.length > 8 ? '' : 'Password must be at least 8 characters long'
      passwordError.value = password.value.length > 8

      if (password.value.length > 8){
        passwordError.value = ''
        sendServer()
      }
      else
        passwordError.value = 'Password must be at least 8 characters long'

    }

    const sendServer = () => {
      axios.post('http://localhost:8000/api/v1', {
        firsName: firstName,
        lastName: lastName,
        email: email,
        password: password,
        role: role,
      })
      .then(resp => {

        console.log(resp + ' risposta')

        toast({
          message: 'Account created, please log in',
          type:'is-success',
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: 'center'
        })

        // router.push({ name: 'Login' })

      })
      .catch(err =>  console.log('error ' + err))

  }

    const returnLogin = () => {
      router.push({ name: 'Login' })
    }

    return{ logo, firstName, lastName, email, password, role, passwordError, handleSubmit, returnLogin }
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
  border-radius: 10px;
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

</style>