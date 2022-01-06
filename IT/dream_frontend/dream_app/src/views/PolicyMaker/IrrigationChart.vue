<template>
  <div style="width: 90%; overflow: scroll; left: 5%; position:relative;">
    <div style="width: 830px; margin-bottom:20px">
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