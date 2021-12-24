<template>
  <h1 class="ale">My name's {{ name }} i'm {{Tage}}</h1>

  <button @click="changeAge">Increase</button>
</template>

<script>

export default {
  name: "Test1",

  props:{
    age: Number,
    name: String
  },

  data() {
    return {
      Tname: this.name.valueOf(),
      Tage: this.age.valueOf(),
    }
  },

  methods: {
    changeAge() {
      this.Tage++
    }
  }
}
</script>

<style scoped>
  .ale {
    color: red;
    background-color: green;
  }
</style>