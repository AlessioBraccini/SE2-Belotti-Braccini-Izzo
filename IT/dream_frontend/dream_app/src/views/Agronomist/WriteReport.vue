<template>

  <NavbarAgro :name="name"/>

  <div class="background">
    <h2>Upload File</h2>
    <div class="text1">You can upload 1 pdf file:</div>
    <div class="fileInput">
      <p class="innerText">Select your file</p>
      <input type="file" @change="handleFileUpload( $event )" required />
    </div>

    <div v-if="errMsg.length" class="errorMsg">
      {{errMsg}}
    </div>

    <div class="text">
      <p class="text2" style="margin-right: 5px;">Uploaded File:</p>
      <p v-if="fileName" class="text2" style="margin-top: 0"> {{ fileName }}</p>
    </div>
  </div>
  <div>
    <button @click="submitFile" class="submitBtn actionButton">Submit</button>
    <button @click="pushReport" class="actionButton backBtn">View Send Report</button>
    <button @click="back" class="actionButton backBtn">Back</button>
  </div>

  <div v-if="confirmationMessage" class="opacityBack">
    <div  class="confirmMsg">
      <h4 class="confirmText"> {{ confirmationMessage }} </h4>
    </div>
  </div>

</template>

<script>
import NavbarAgro from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";
import NProgress from "nprogress"


export default {
  name: "WriteReport",
  props: ['n'],
  components: {NavbarAgro},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const file = ref('')
    const fileName = ref('')
    const confirmationMessage = ref('')
    const errMsg = ref('')

    // Upload to the web server the file that want to send to the server
    const handleFileUpload = (event) => {
      file.value = event.target.files[0]
      fileName.value = event.target.files[0].name
      if (fileName.value.length)
        errMsg.value = ''
    }

    // Submit the file to the server and check that it is a pdf file
    const submitFile =  () => {
      NProgress.start()
      if (fileName.value.length) {
        const ext = fileName.value.slice(fileName.value.length-3,fileName.value.length)
        if (ext === 'pdf'){
          let formData = new FormData();
          formData.append('file', file.value);
          formData.append('title', fileName.value)

          axios.post('https://appdream.herokuapp.com/api/v1/steering_initiatives',
              formData,
              {
                headers: {
                  'Content-Type': 'multipart/pdf'
                }
              })
              .then(() => {
                NProgress.done()
                scroll(0, 0)
                confirmationMessage.value = 'Successful send'

                setTimeout(function () {
                  router.push({name: 'AgroHome'})
                }, 1250);
              })
              .catch(err => {
                console.log('FAILURE!! ' + err);
              });
        }
        else
          errMsg.value = '!You can upload only pdf file'
      }
      else
        errMsg.value = '!No file selected'

    }

    const pushReport = () => {
      router.push({ name: 'ViewReport' })
    }

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    return{name, file, fileName, confirmationMessage, errMsg, submitFile, handleFileUpload, back, pushReport}
  }
}
</script>

<style scoped>

  input{
    height: 100%;
    width: 100%;
    opacity: 0;
    z-index: 99;
    position: relative;
  }

  h2{
    position: relative;
    left: 9%;
    max-width: 80%;
    padding-top: 15px;
    margin: 0;
  }

  .background{
    background-color: #E9C197;
    position: relative;
    border-radius: 10px;
    width: 90%;
    left: 6%;
    height: auto;
    top: 15px;
  }

  .text1{
    position: relative;
    left: 9%;
    max-width: 80%;
    margin-top: 5px;
    margin-bottom: 15px;
    color: #5a5a5a;
  }

  .text{
    position: relative;
    left: 9%;
    max-width: 80%;
  }

  .text2{
    position: relative;
    left: 0;
    max-width: 80%;
    display: inline-block;
  }

  .fileInput{
    position: relative;
    border: solid 2px #919191;
    border-radius: 10px;
    width: 80%;
    height: 100px;
    left: 9%;
  }

  .innerText{
    position: absolute;
    left: 30%;
    top: 20%;
    z-index: 98;
  }

  .submitBtn{
    width: 90%;
    left: 6%;
    margin-top: 6%;
  }

  .backBtn{
    width: 90%;
    left: 6%;
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

  .errorMsg{
    position: relative;
    color: red;
    left: 9%;
    margin-top: 5px;
  }

  @media only screen and (min-width: 930px) {

    .background{
      width: 70%;
      left: 16%;
      margin-top: 5%;
    }

    .backBtn, .submitBtn {
      width: 20%;
      margin-right: 5%;
      left: 16%;
      margin-top: 5%;
      margin-bottom: 2%;

    }
  }

</style>
