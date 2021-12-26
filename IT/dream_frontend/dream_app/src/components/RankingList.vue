<template>
  <div class="square">
    <div v-if="error">{{ error }}</div>
    <div v-if="farmerList.length">
      <!--display ranking component-->
    </div>
    <div v-else class="rawText">Loading...</div>
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  name: "RankingList",

  setup(){

    const farmerList = ref([])
    const error = ref(null)

    const load = async () => {
      try {
        let data = await fetch('url dell\' api del server backend')
        if (!data.ok) {
          throw Error('error data fetching ranking list')
        }

        // farmerList.value = await data   retrieve data from data
        // use these data
      }
      catch (err){
        error.value = err.message
        console.log(err.message)
        // can put the error in the template with the v-if
      }
    }

    load()

    return{ farmerList, error }

  }

}
</script>

<style scoped>
  .square{
    position: relative;
    display: block;
    background-color: #E9C197;
    width: 90%;
    height: 290px;
    left: 5%;
    top: 5%;
    border-radius: 22px;
    margin-top: 20px;
  }

  .rawText{
    position: relative;
    top: 45%;
    left: 39%;
    width: 100px;
  }
</style>