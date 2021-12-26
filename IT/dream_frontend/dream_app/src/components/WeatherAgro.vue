<template>

  <div class="square">
    <p class="rawText">{{area}}</p>
  </div>

</template>

<script>
export default {
  name: "WeatherAgro",

  props: ['area'],
}
</script>

<style scoped>

  .square{
    position: relative;
    display: block;
    background-color: #E9C197;
    width: 90%;
    height: 200px;
    left: 5%;
    top: 5%;
    border-radius: 22px;
  }
  .rawText{
    position: relative;
    top: 45%;
    left: 39%;
    width: 100px;
  }

</style>