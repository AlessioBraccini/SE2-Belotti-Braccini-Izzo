<template>

  <router-view/>

</template>

<script>

export default {
  name: 'App',
  components: {
  }


}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
  background-color: #faf4d3;
  font-size: calc(10px + 2vmin);
  width: 100%;
  position: fixed;
  z-index: 1;
}

.actionButton{
  position: relative;
  width: 80%;
  min-height: 50px;
  background-color: #004643;
  border-radius: 10px;
  color: white;
  margin-top: 10px;
  font-size: 22px;
}

.divProfileImg{
  position: relative;
  display: inline-block;
  width: 40px;
  height: 40px;
  left: 5%;
  top: 10px;
}

.profileImg{
  width: 40px;
  height: 40px;
  border-radius: 20px;
}



.welcomeMessage{
  position: relative;
  width: 80px;
  color: gray;
  margin: 0;
}

.usernameStyle{
  position: relative;
  width: 80px;
  color: black;
  margin: 0;
}

.menuButton{
  display: inline-block;
  position: relative;
  width: 40px;
  height: 40px;
  left: 45%;
  border-radius: 20px;
  background-color: #004643;
  font-size: 30px;
  color: white;
}

.initialPage{
  position: relative;
  min-height: 550px;
}

.inputFieldContainer{
  position: relative;
  top: 200px;
  left: 10%;
}

.inputField{
  position: relative;
  width: 80%;
  min-height: 50px;
  margin-top: 8px;
  font-size: 22px;
}

.remMeDiv{
  position: relative;
}

.checkType{
  position: relative;
  display: inline-block;
  margin-top: 10px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: 3px solid gray;
  appearance: none;
  -webkit-appearance: none;
}

.remMeLbl{
  display: inline-block;
  position: relative;
  top: -7px;
  font-size: 22px;
}

.checkType:checked{
  background-color: gray;
  appearance: initial;
}

.initialButton{
  position: relative;
}

</style>