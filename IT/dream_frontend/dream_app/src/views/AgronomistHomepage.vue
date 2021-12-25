<template>
  <NavbarAgro :name="name"/>
  agro home
</template>

<script>
import NavbarAgro from "@/components/NavbarAgro";
import {ref} from "vue";

export default {
  name: "AgronomistHomepage",
  components: {NavbarAgro},
  setup(){

    const name = ref('karun')

    // load user data from api

    return{ name }
  }
}
</script>

<style scoped>

</style>