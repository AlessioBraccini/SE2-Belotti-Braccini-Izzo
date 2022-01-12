<template>
  <NavbarAgro :name="name"/>

  <div class="square">

    <div class="date">{{ request['date'] }}</div>
    <div class="subject">Subject: {{ request['subject'] }}</div>
    <div class="name">From: {{ request['sender_name'] }}</div>

    <p>Message:</p>
    <div class="message">
      {{ request['message'] }}
    </div>

    <div class="line"/>

<!--    <div class="message" style="margin-top: 20px;">-->
<!--      Subject:-->
<!--      <input type="text" class="textInput" v-model="subject"/>-->
<!--    </div>-->

    <div class="reply">
      Reply:
      <textarea v-model="message"/>
    </div>

    <div style="height: 15px"/>

  </div>

  <button @click="send" class="actionButton backBtn">Send</button>
  <button @click="back" class="actionButton backBtn">Back</button>

  <div v-if="confirmationMessage" class="opacityBack">
    <div  class="confirmMsg">
      <h4 class="confirmText"> {{ confirmationMessage }} </h4>
    </div>
  </div>

</template>

<script>
// import axios from "axios";

import axios from "axios";
import {ref} from "vue";
import NavbarAgro from "@/views/Navbar";
import router from "@/router";

export default {
  name: "ReplyRequest",
  components: {NavbarAgro},
  setup(){

    const name = localStorage.getItem('name')
    const request = ref('')
    const error = ref('')
    const confirmationMessage = ref('')
    const subject = ref('')
    const message = ref('')

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadRequests =  async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/help_request_by_id', {params:{request_id: localStorage.getItem('id')}})
            .then(resp => {
              request.value = resp.data
        }).catch(() => {
          error.value = 'No message for you'
        })
      }
      catch(err) {
        error.value = err.toString()
      }
    }

    loadRequests()

    const send =  async () => {
      try {
        await axios.post('http://localhost:8000/api/v1/help_request', {
          reply: message.value,
          request_id: localStorage.getItem('id')
        }).then(() => {
          scroll(0,0)
          confirmationMessage.value = 'Message send successfully'

          setTimeout(function() {
            router.push({name: 'AgroHome'})
          }, 1250);
        }).catch(() => {
          console.log('error')
        })
      }
      catch(err) {
        console.log('err load ' + err)
        // can put the error in the template with the v-if
      }
    }

    const back = () => {
      router.go(-1)
    }

    return{ name, request, subject, message, confirmationMessage, back, send }
  }
}
</script>

<style scoped>

  p{
    position: relative;
    margin: 0;
    left: 6%;
    width: 100px;
    color: #7a7a7a;
  }

  .subject{
    position: relative;
    left: 6%;
    text-align: left;
    width: 90%;
    font-weight: bold;
    font-size: 25px;
    margin-top: 10px;
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

  .date{
    position: relative;
    text-align: right;
    color: #7a7a7a;
    left: 5%;
    width: 90%;
    padding-top: 5px;

  }

  .name{
    position: relative;
    left: 6%;
    width: 90%;
    margin-top: 5px;
  }

  .message{
    position: relative;
    left: 6%;
    margin-top: 5px;
    width: 90%;
  }

  .line{
    position: relative;
    width: 85%;
    border: #919191 1px dashed;
    left: 6%;
    margin-top: 15px;
  }

  .reply{
    position: relative;
    margin-top: 15px;
    left: 6%;
    width: 90%;
  }

  textarea{
    height: 200px;
    width: 95%;
    border-radius: 10px;
    resize: none;
  }

  .backBtn{
    width: 90%;
    left: 5%;
  }

  .confirmMsg{
    position: absolute;
    z-index: 999;
    width: 80%;
    height: 100px;
    background-color: #E9C197;
    text-align: center;
    border: #919191 2px solid;
    border-radius: 10px;
    left: 8%;
    top: 40%;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    color: black;
  }

  .confirmText{
    position: relative;
    top: 35px;
    margin: 0;
  }

  .opacityBack{
    z-index: 99;
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: rgba(40, 70, 70, 0.8);
    top: 0;
    display: block;
  }

  @media only screen and (min-width: 612px) {

    .backBtn {
      width: 40%;
      margin-right: 10%;
      left: 5%;
      margin-top: 2%;
      margin-bottom: 2%;
    }
  }

</style>