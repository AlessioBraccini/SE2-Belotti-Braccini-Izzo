<template>
  <div class="container">
    <p style="text-align: center">Soil Humidity and Average Temperature</p>
    <div class="inner">
      <canvas id="humidityChart"></canvas>
      <p style="text-align: center">Average Humidity: {{ avgHumidity.toFixed(2) }}</p>
      <p style="text-align: center">Average Temperature: {{ avgTemp.toFixed(2) }}</p>
    </div>

  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import axios from "axios";
import {ref} from "vue";

export default {
  name: 'HumidityChart',

  setup(){
    let avgHumidity = ref(0)
    let avgTemp = ref(0)
    return {avgHumidity, avgTemp}
  },

  async mounted() {

    let hum, temp

    // Retrieve the humidity chart data and store them in hum variable
    const getHumidity = async () => {
      await axios.get('https://appdream.herokuapp.com/api/v1/humidity').then(resp => {
        hum = resp.data.humidity
        for (let i = 0; i < resp.data.humidity.length; i++) {
          this.avgHumidity += resp.data.humidity[i]
        }
        this.avgHumidity /= resp.data.humidity.length
      })
      return hum
    }

    // Retrieve the temperature chart data and store them in temp variable
    const getTemp = async () => {
      await axios.get('https://appdream.herokuapp.com/api/v1/humidity').then(resp => {
        temp = resp.data.temperature
        for (let i = 0; i < resp.data.temperature.length; i++) {
          this.avgTemp += resp.data.temperature[i]
        }
        this.avgTemp /= resp.data.temperature.length
      })
      return temp
    }

    // Create the graph
    const ctx = document.getElementById('humidityChart');
    new Chart(ctx,{
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
          {   type: 'bar',
            label: "Humidity (%)",
            data: await getHumidity(),
            backgroundColor: "rgba(54,73,93,.5)",
            borderColor: "#36495d",
            borderWidth: 3
          },
          {
            type: 'line',
            label: "Temperature (°C)",
            data: await getTemp(),
            backgroundColor: "red",
            borderColor: "red",
            borderWidth: 3,
          }
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
            max: 100
          },

          y1: {
            type: 'linear',
            position: 'right',
            max: 100,
            min: 0,
            grid: {
              drawOnChartArea: false,
            },
          }
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
    width: 860px;
    margin-bottom:20px;
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