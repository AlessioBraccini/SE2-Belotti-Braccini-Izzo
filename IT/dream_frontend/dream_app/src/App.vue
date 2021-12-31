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
    font-family: Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    height: auto;
  }

  body {
    background-color: #faf4d3;
    font-size: calc(10px + 2vmin);
    width: 99%;
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

  .confirmMsg{
    position: absolute;
    z-index: 999;
    width: 40%;
    height: 60px;
    background-color: #004643;
    text-align: center;
    border: #919191 2px solid;
    border-radius: 10px;
    left: 5%;
    top: 80%;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    color: #faf4d3;
  }
</style>