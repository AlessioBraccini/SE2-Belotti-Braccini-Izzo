<template>

  <div class="square">
    <h3 class="title">Weather</h3>

    <div class="area">
      <img src="@/assets/profile.png"/>
      <h3 class="areaText">{{ area }}</h3>
    </div>

    <div class="temperature">
      <img src="@/assets/profile.png"/>
      <p>{{temperatureValue}}°C</p>
    </div>

    <div class="tempMax">
      <img src="@/assets/profile.png"/>
      <p>{{temperatureHigh}}°C</p>
    </div>

    <div class="wind">
      <img src="@/assets/profile.png"/>
      <p>{{windSpeed}} Kph</p>
    </div>

    <div class="humidity">
      <img src="@/assets/profile.png"/>
      <p>{{humidity}}%</p>
    </div>

    <div class="tempMin">
      <img src="@/assets/profile.png"/>
      <p>{{temperatureLow}}°C</p>
    </div>

    <div class="cloud">
      <img src="@/assets/profile.png"/>
      <p>{{cloudiness}}</p>
    </div>

<!--    <div class="description">-->
<!--      <p>{{description}}</p>-->
<!--    </div>-->
  </div>

</template>

<script>

// import axios from "axios";
import {ref} from "vue";

export default {
  name: "WeatherAgro",
  props: ['area'],

  setup(){

    // 547eaf1664e44666701371efa7605159
    // api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}

    const cloudiness =ref(0);
    const windSpeed =ref(0);
    const humidity =ref(0);

    const temperatureValue =ref(0);
    const temperatureHigh =ref(0);
    const temperatureLow =ref(0);

    const description = ref('');



    const loadWeather = async () => {

      await fetch('https://api.openweathermap.org/data/2.5/weather?q='+ localStorage.getItem('district') +'&units=metric&appid=547eaf1664e44666701371efa7605159')
          .then( resp => resp.json())
          .then( data => {

            cloudiness.value = data.clouds.all
            windSpeed.value = data.wind.speed
            humidity.value = data.main.humidity
            temperatureValue.value = Math.round(data.main.temp)
            temperatureHigh.value = Math.round(data.main.temp_max)
            temperatureLow.value = Math.round(data.main.temp_min)
            description.value = data.weather[0].description

          })

    }

    loadWeather()

    return{ cloudiness, windSpeed, humidity, temperatureValue, temperatureHigh, temperatureLow, description }

  }
}
</script>

<style scoped>

  div{
    width: 30%;
    display: inline-block;
    left: 6%;
  }

  img{
    position: relative;
    width: 24px;
    height: 24px;
    display: inline-block;
    margin-right: 10px;
    top: 6px;
  }

  p{
    display: inline-block;
  }

  h3{
    margin: 20px 0 0 0;
  }

  .areaText{
    display: inline-block;
    margin-top: 3%;
    margin-bottom: 3%;
  }

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

  .title{
    position: relative;
    top: 10px;
    text-align: center;

  }

  .area{
    position: relative;
    width: 90%;
    top: 5%;
    left: 5%;
    text-align: center;

  }

  .cloud{
    position: relative;
    /*top: 30%;*/
    /*left: -60%;*/
  }

  .wind{
    position: relative;
    /*top: 55%;*/
    /*left: -73%;*/
  }

  .humidity{
    position: relative;
    /*top: 0;*/
    /*left: 28%;*/
  }

  .temperature{
    position: relative;
    /*top: 25%;*/
    /*left: 15%;*/
  }

  .tempMax{
    position: relative;
    /*top: 1px;*/
    /*left: 25%;*/
  }

  .tempMin{
    position: relative;
    /*top: 25%;*/
    /*left: 12%;*/
  }

  .description{
    position: relative;
    /*top: 1%;*/
    /*left: 1%;*/
  }


</style>