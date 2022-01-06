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
    <div v-else class="rawText">Loading...</div>
  </div>

  <button @click="back" class="actionButton backBtn">Back</button>

</template>

<script>
import Navbar from "@/views/Navbar";
import {ref} from "vue";
import axios from "axios";
import router from "@/router";

export default {
  name: "ViewReport",
  components: {Navbar},

  setup(){

    const name = ref(localStorage.getItem('name'))
    const reportList = ref([])
    const error = ref(null)

    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

    const loadReport = async () => {
      try {
        await axios.get('http://localhost:8000/api/v1/steering_initiatives').then(resp => {
          reportList.value = resp.data['reports_list']
        })
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
      }
    }

    loadReport()

    const viewSpecificReport = async (report) => {
      console.log(report)
      await axios.get('http://localhost:8000/api/v1/download_reports',
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
          }
      ).catch(err => {
        console.log(err)
      })

    }

    const back = () => {
      router.push({name: 'PMHome'})
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

</style>