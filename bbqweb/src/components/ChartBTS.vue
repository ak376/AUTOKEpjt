<template>
  <div class="BTS">
    <h1>{{ msg }}</h1>
    <p>
         beta ver. 1.1
    </p>
    <apexchart width="500" type="line" :options="options" :series="series" />
  </div>
</template>

<script>
import io from 'socket.io-client'
import VueApexCharts from 'vue-apexcharts'
import moment from 'moment'

export default {
  name: 'ChartBTS',
  props: {
    msg: String
  },
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      socket: '',
      time: [],
      temperatures: [],
      humidities: [],
      pressures: [],
      options: {},
      series: [],
    }
  },
  created() {    
    this.socket = io("http://localhost:3000"); 
    this.socket.on("fromser", (arg)=> {
        console.log(arg);
        this.times = arg.map((x) => moment(x.time).format("HH:mm"));
        this.temperatures = arg.map((x) => x.num1);
        this.humidities = arg.map((x) => x.num2);
        this.pressures = arg.map((x) => x.num3);
        this.options = {
          xaxis: {
            categories: this.times,
          }
        };
        this.series = [
          {
            name: "압력: Pa",
            data: this.temperatures,
          },
          {
            name: "온도: °C",
            data: this.humidities,
          },
          {
            name: "습도: %",
            data: this.pressures,
          }
        ]
    });

    this.socket.emit("bbq", "is soso");
  }
  
}
</script>

<style scoped>
</style>