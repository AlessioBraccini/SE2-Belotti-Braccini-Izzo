<template>

  <NavbarAgro :name="name"/>

  <div class="background">
    <h2 class="text1">Upload File</h2>
    <div class="fileInput">
      <p class="innerText">Select your file</p>
      <input type="file" @change="handleFileUpload( $event )" required />
    </div>

    <div class="text">
      <p class="text2" style="margin-right: 5px">Uploaded File:</p>
      <p v-if="fileName" class="text2"> {{ fileName }}</p>
    </div>
  </div>
  <div>
    <button @click="submitFile" class="submitBtn actionButton">Submit</button>
    <button @click="back" class="actionButton backBtn">Back</button>
  </div>

</template>

<script>
import NavbarAgro from "@/views/Agronomist/NavbarAgro";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";

export default {
  name: "WriteReport",
  props: ['n'],
  components: {NavbarAgro},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const file = ref('')
    const fileName = ref('')


    const handleFileUpload = (event) => {
      file.value = event.target.files[0]
      fileName.value = event.target.files[0].name
      console.log(fileName.value)
    }

    const submitFile =  () => {
      let formData = new FormData();
      formData.append('file', file.value);

      axios.post( 'url',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(resp => {
            console.log('SUCCESS!! ' + resp);
          })
           .catch(err => {
                console.log('FAILURE!! ' + err);
           });
    }

    const back = () => {
      router.push({name: 'AgroHome'})
    }

    return{name, file, fileName, submitFile, handleFileUpload, back}
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
    margin-top: 15px;
    display: inline-block;
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

</style>
