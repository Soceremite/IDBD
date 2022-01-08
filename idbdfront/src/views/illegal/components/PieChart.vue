<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/vintage') // echarts theme
import resize from '@/components/Charts/mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '500px'
    },
    piechartdata:{
      type:Array,
      default:[]
    }
  },
  data() {
    return {
      chart: null,
      lineOption:{
        backgroundColor: '#ecf0f3',
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: ['喝水', '抽烟', '玩手机', '疲劳驾驶']
        },
        series: [
          {
            name: '违规驾驶记录',
            type: 'pie',
            roseType: 'radius',
            radius: ['30%','80%'],
            center: ['50%', '38%'],
            data: [
              { value: 0, name: '喝水' },
              { value: 0, name: '抽烟' },
              { value: 0, name: '玩手机' },
              { value: 0, name: '疲劳驾驶' }
            ],
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  watch: {
    piechartdata: function(newVal, oldVal) {
      console.log(newVal, oldVal)
      this.chart.clear()
      console.log('重载')
      for(var i=0;i<4;i++)
      {
        this.lineOption.series[0].data[i].value = this.piechartdata[i]
      }
      this.chart.setOption(this.lineOption, true)
    },
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'vintage')

      this.chart.setOption(this.lineOption)
    }
  }
}
</script>
