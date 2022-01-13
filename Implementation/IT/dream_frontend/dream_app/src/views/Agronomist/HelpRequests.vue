<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <h3>Farmers Requests</h3>

    <div class="farmerArea">

      <div v-if="error" class="errorMsg">{{ error }}</div>
      <div v-else-if="requests.length" style="height: 70%">
        <div class="farmerName">
          <ul>
            <li v-for="msg in requests.length" :key="msg" @click="openMsg(requests[msg-1])">
              <div class="list">{{ requests[msg-1]['date'] }} </div>
              <div class="list">From: {{ requests[msg-1]['sender_name'] }}</div>
              <div class="list">Subject: {{ requests[msg-1]['subject'] }}</div>
            </li>
          </ul>
        </div>
      </div>
      <div v-else class="rawText">Loading...</div>
    </div>

    <div style="height: 20px"/>

  </div>

  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import {ref} from "vue";
import axios from "axios";
import router from "@/router";
import NavbarAgro from "@/views/Navbar";


export default {
  name: "HelpRequests",
  components: {NavbarAgro},
  setup(){
    const name = localStorage.getItem('name')
    const requests = ref([])
    const error = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadRequests =  async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/help_request').then(resp => {
          requests.value = resp.data
        }).catch(() => {
          error.value = 'No message for you'
        })
      }
      catch(err) {
        error.value = err.toString()
      }
    }

    loadRequests()

    const openMsg = (id) => {
      localStorage.setItem('id', id['request_id'])
      router.push({name: 'ReplyReq'})
    }

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    return{ name, requests, error, back, openMsg }

  }
}
</script>

<style scoped>

  h3{
    margin: 0;
    padding: 10px 0 0 21px;
    height: 10%;
    left: 5%;
    text-align: left;
  }

  ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  li{
    margin-bottom: 10px;
    border-bottom: solid #919191 1px;
    cursor: pointer;
  }

  li:hover{
    background-color: #004643;
    color: #ffffff;
    border-radius: 5px;
    padding-left: 10px;
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
  }

  .farmerArea{
    position: relative;
    display: block;
    background-color: white;
    width: 90%;
    height: 580px;
    left: 5%;
    border-radius: 22px;
    overflow-y: scroll;
  }

  .rawText{
    position: relative;
    top: 45%;
    left: 24%;
    width: 165px;
  }

  .farmerName{
    position: relative;
    display: inline-block;
    width: 90%;
    left: 5%;
    top: 5%;
    font-weight: bold;
  }

  .list{
    margin-bottom: 5px;
    max-width: 100%;
  }

  .backBtn{
    width: 90%;
    left: 5%;
    margin-bottom: 20px;
  }

  .errorMsg {
    position: relative;
    color: red;
    text-align: center;
    top: 45%;
  }
</style>