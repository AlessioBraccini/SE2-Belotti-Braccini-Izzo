<template>
  <div class="container">
    <div class="inner">
      <canvas id="irrigationChart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import irrigationData from './IrrigationData.js'

export default {
  name: 'IrrigationChart',
  data() {
    return {
      data: irrigationData
    }
  },
  mounted() {
    const ctx = document.getElementById('irrigationChart');
    new Chart(ctx, this.data);
  }

}
</script>

<style scoped>
  .container{
    position:relative;
    width: 90%;
    overflow: scroll;
    left: 5%;
    background-color: white;
    border-radius: 22px;
    margin-top: 20px;
  }
  .inner{
    width: 840px;
    margin-bottom:20px
  }
</style>