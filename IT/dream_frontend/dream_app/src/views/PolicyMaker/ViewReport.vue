<template>
  <Navbar :name="name"/>

  <div class="square">

    <h3>Steering Initiative</h3>

    <div v-if="error" style="text-align: center">{{ error }}</div>
    <div v-else-if="reportList.length" class="scrollDiv">
      <div>
        <div class="farmerName">
          <ul>
            <li v-for="report in reportList.length" :key="report" @click="viewSpecificReport(reportList[report-1])">
              <div>{{ reportList[report-1]['author'] }}</div>
              <div>{{ reportList[report-1]['file_name'] }}</div>
              <div>{{ reportList[report-1]['pub_date'] }}</div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else class="rawText">No Reports Available</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";
import NProgress from "nprogress"
import {serverUrl} from "../../../config";

export default {
  name: "ViewReport",
  components: {Navbar},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const reportList = ref([])
    const error = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    // Download the list steering initiative from the server
    const loadReport = async () => {
      try {
        await axios.get(serverUrl + '/api/v1/steering_initiatives').then(resp => {
          reportList.value = resp.data['reports_list']
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    loadReport()

    // Retrieve and download the specific report using the author_id, the publication date and the file name
    const viewSpecificReport = async (report) => {
      NProgress.start()
      await axios.get(serverUrl + '/api/v1/download_reports',
          { responseType: "blob",
            params: {
              author_id: report['author_id'],
              pub_date: report['pub_date'],
              file_name: report['file_name']
            } }
      ).then(
          resp => {
            console.log('risposta ' + resp.data)

            const blob = new Blob([resp.data], { type: "application/pdf" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = report['file_name'];
            link.click();
            URL.revokeObjectURL(link.href);

            NProgress.done()
          }
      ).catch(err => {
        console.log(err)
        if (err.response.status === 401){
          NProgress.done()
          localStorage.clear()
          localStorage.setItem('reload', null)
          alert("You lost the connection please log in again");
          router.push({name: 'Login'})
        }
      })

    }

    const back = () => {
      switch (localStorage.getItem('role')){
        case 'A': router.push({name: 'WriteReport'}); break;
        case 'P': router.push({name: 'PMHome'}); break;
        case 'F': router.push({name: 'FarmerHome'}); break;
      }
    }

    return{ name, reportList, error, back, viewSpecificReport }
  }
}
</script>

<style scoped>

  h3{
    margin: 0;
    padding: 10px 0 0 0;
    height: 5%;
    text-align: center;
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
    height: 620px;
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
  }

  .rawText{
    position: relative;
    text-align: center;
  }

  .scrollDiv{
    height: 90%;
    overflow-y: scroll;
  }

  .farmerName{
    position: relative;
    display: inline-block;
    width: 86%;
    left: 7%;
    top: 5%;
    font-weight: bold;

  }

  .backBtn{
    width: 90%;
    left: 5%;
    margin-top: 20px;
  }

  @media only screen and (min-width: 600px){
    .backBtn{
      margin-bottom: 2%;
    }
  }

</style>