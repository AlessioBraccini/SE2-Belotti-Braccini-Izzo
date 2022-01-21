<template>
  <div class="container">
    <p style="text-align: center">Water used for Irrigation</p>
    <div class="inner">
      <canvas id="irrigationChart"></canvas>
      <p style="text-align: center">Total amount of water: {{ totalWater }} t</p>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import axios from "axios";
import {ref} from "vue";

export default {
  name: 'IrrigationChart',

  setup(){
    let totalWater = ref(0)
    return {totalWater}
  },

  async mounted() {

    let irr

    // Retrieve the chart data and store them in irr variable
    const getIrrigation = async () => {
      await axios.get('https://appdream.herokuapp.com/api/v1/water_irrigation').then(resp => {
        irr = resp.data.water_qty
        for (let i = 0; i < resp.data.water_qty.length; i++) {
          this.totalWater += resp.data.water_qty[i]
        }
      })
      return irr
    }

    // Create the graph
    const ctx = document.getElementById('irrigationChart');
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: [
          'Adilabad',
          'Bhadradri Kothagudem',
          'Hanumakonda',
          'Hyderabad',
          'Jagtial',
          'Jangaon',
          'Jayashankar Bhupalpally',
          'Jogulamba Gadwal',
          'Kamareddy',
          'Karimnagar',
          'Khammam',
          'Kumuram Bheem',
          'Mahabubabad',
          'Mahabubnagar',
          'Mancherial',
          'Medak',
          'Medchal-Malkajgiri',
          'Mulugu',
          'Nagarkurnool',
          'Nalgonda',
          'Narayanpet',
          'Nirmal',
          'Nizamabad',
          'Peddapalli',
          'Rajanna Sircilla',
          'Rangareddy',
          'Sangareddy',
          'Siddipet',
          'Suryapet',
          'Vikarabad',
          'Wanaparthy',
          'Warangal',
          'Yadadri Bhuvanagiri'],
        datasets: [
          { type: 'bar',
            label: "Used Water (t)",
            data: await getIrrigation(),
            backgroundColor: "rgba(54,73,93,.5)",
            borderColor: "#36495d",
            borderWidth: 3
          },
        ]
      },
      options: {
        responsive: true,
        lineTension: 0,
        layout: {
          padding: 20
        },
        scales: {
          y:{
            type: 'linear',
            position: 'left',
            min: 0,
            max: 10000
          },
        },
      },
    });
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
    width: 855px;
    margin-bottom:20px
  }

  @media only screen and (min-width: 995px) and (max-width: 1200px) {
    .container{
      overflow: hidden;
    }
  }

  @media only screen and (min-width: 1200px) and (max-width: 1550px){
    .container{
      overflow: hidden;
    }
    .inner{
      margin-left: 18%;
    }
  }

  @media only screen and (min-width: 1550px) {
    .container{
      overflow: hidden;
    }
    .inner{
      margin-left: 24%;
    }
  }
</style>