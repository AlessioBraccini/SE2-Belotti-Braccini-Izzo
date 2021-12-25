<template>
  <div v-if="error">{{ error }}</div>
  <div v-if="farmerList.length">
    <!--display ranking component-->
  </div>
  <div v-else>Loading...</div>
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

</style>