<template>
  <img src="../assets/dramLogo.png" alt="DREAM" class="image">

  <form @submit.prevent="handleSubmit">
    <input type="text" required v-model="firstName" placeholder="First Name" class="textInput">

    <input type="text" required v-model="lastName" placeholder="Last Name" class="textInput">

    <input type="email" required v-model="email" placeholder="Email" class="textInput">

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
export default {
  name: "LoginForm",

  data(){
    return{
      firstName:'',
      lastName:'',
      email:'',
      password:'',
      role:'policyMaker',
      passwordError:''
    }
  },

  methods:{
    handleSubmit(){
      this.passwordError = this.password.length > 8 ? '' : 'Password must be at least 8 characters long'

      //call backend function
    },

    returnLogin() {
      this.$router.push({ name: 'Login' })
    }
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
}

.error{
  position: relative;
  width: 80%;
  left: 8%;
  font-size: 14px;
  margin: -10px 0 10px 0;
}

</style>