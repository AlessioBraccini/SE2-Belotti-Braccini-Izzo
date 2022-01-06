<template>
  <div style="width: 90%; overflow: scroll; left: 5%; position:relative;">
    <div style="width: 830px; margin-bottom:20px">
      <canvas id="humidityChart" style=""></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import humidityData from './HumidityData.js'

export default {
  name: 'HumidityChart',
  data() {
    return {
      data: humidityData
    }
  },
  mounted() {
    const ctx = document.getElementById('humidityChart');
    new Chart(ctx, this.data);
  }

}
</script>