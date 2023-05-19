<template>
  <div class="BTS">
    <h1>{{ msg }}</h1>
    <p>
        BTS는 샴푸가 아닙니다.
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
    this.socket.on("kfc", (arg)=> {
        console.log(arg);
        this.times = arg.map((x) => moment(x.time).format("HH:mm:ss"));
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
            name: "온도",
            data: this.temperatures,
          },
          {
            name: "습도",
            data: this.humidities,
          },
          {
            name: "대기압",
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