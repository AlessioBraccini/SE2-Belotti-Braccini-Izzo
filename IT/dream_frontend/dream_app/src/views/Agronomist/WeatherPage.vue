<template>
  <NavbarAgro :name="name"/>
  <div class="container">
    <div class="square">

      <div class="area">
        <img src="@/assets/icon/positionIcon.png"/>
        <h3 class="areaText">{{ area }}</h3>
      </div>

      <div class="temperature">
        <p>{{temperatureValue}}°C</p> <br>
        <p class="description" >{{description}}</p>
      </div>

      <div class="humidity">
        <img src="@/assets/icon/humidityIcon.png"/>
        <p>Humidity: {{humidity}}%</p>
      </div>

      <div class="humidity">
        <img src="@/assets/icon/pressureIcon.png"/>
        <p>Pressure: {{pressure}} mbar</p>
      </div>

      <div class="tempMax">
        <img src="@/assets/icon/maxIcon.png"/>
        <p>Max temperature: {{temperatureHigh}}°C</p>
      </div>

      <div class="tempMin">
        <img src="@/assets/icon/minIcon.png"/>
        <p>Min temperature: {{temperatureLow}}°C</p>
      </div>

      <div class="wind">
        <img src="@/assets/icon/windIcon.png"/>
        <p>Wind speed: {{windSpeed}} Kph</p>
      </div>

      <div class="wind">
        <img src="@/assets/icon/directionIcon.png"/>
        <p>Wind direction: {{windDeg}}°</p>
      </div>

      <div class="cloud">
        <img src="@/assets/icon/cloudIcon.png"/>
        <p>Cloudiness: {{cloudiness}}</p>
      </div>
    </div>

    <button @click="back" class="actionButton backBtn">Back</button>
  </div>

</template>

<script>

// import axios from "axios";
import {ref} from "vue";
import NavbarAgro from "@/components/NavbarAgro";
import router from "@/router";

export default {
  name: "WeatherAgro",
  components: {NavbarAgro},

  setup(){

    // 547eaf1664e44666701371efa7605159
    // api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}

    const name = localStorage.getItem('name')
    const area = localStorage.getItem('district')

    const cloudiness =ref(0);
    const windSpeed =ref(0);
    const windDeg =ref(0);
    const humidity =ref(0);
    const pressure =ref(0);

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
            windDeg.value = data.wind.deg
            humidity.value = data.main.humidity
            pressure.value = data.main.pressure
            temperatureValue.value = Math.round(data.main.temp)
            temperatureHigh.value = Math.round(data.main.temp_max)
            temperatureLow.value = Math.round(data.main.temp_min)
            description.value = data.weather[0].description
          })

    }

    loadWeather()

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    return{ name, area, cloudiness, windSpeed, humidity, temperatureValue, temperatureHigh, temperatureLow, description, windDeg, pressure, back }

  }
}
</script>

<style scoped>

  div{
    width: 90%;
    left: 6%;
    margin-top: 30px;
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
    margin: 0;
  }

  .container{
    margin: 0;
    left: 0;
    width: 100%;
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
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
    margin-bottom: 15px;
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
    padding-bottom: 18px;
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
    top: 25%;
    left: 5%;
    text-align: center;
    font-size: 50px;
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
    font-size: 25px;
    top: -15%;
    text-transform: capitalize;
  }

  .backBtn{
    position: relative;
    left: 5%;
    width: 90%;
    margin: 0;
  }


</style>