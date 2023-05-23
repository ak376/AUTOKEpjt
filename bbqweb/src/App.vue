<template>
  <div id="app">
    <ChartBTS msg="AUTOKE"/>
  
  </div>
</template>

<script>
import ChartBTS from './components/ChartBTS.vue'


export default {
  name: 'App',
  components: {

    ChartBTS
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
