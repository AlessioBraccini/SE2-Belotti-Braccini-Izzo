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
  height: auto;
}

body {
  background-color: #faf4d3;
  font-size: calc(10px + 2vmin);
  width: 100%;
  z-index: 1;
  height: auto;
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

.welcomeMessage{
  position: relative;
  width: 80px;
  color: gray;
  margin: 0;
}

</style>