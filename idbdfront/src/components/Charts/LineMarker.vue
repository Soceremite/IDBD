<template>
  <div :id="id" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '200px'
    },
    height: {
      type: String,
      default: '200px'
    },
    axisx:{
      type:Array,
      default:()=>[]
    },
    axisxtitle:{
      type: String,
      default: '分'
    },
    axisy:{
      type:Array,
      default:()=>[]
    },
    titles:{
      type:String,
      default:''
    },
    emptyshow:{
      type:Boolean,
      default:true
    }
  },
  data() {
    return {
      chart: null,
      lineOption:{
        backgroundColor: '#394056',
        title: {
          top: 20,
          text: '驾驶员违规历史展示',
          textStyle: {
            fontWeight: 'normal',
            fontSize: 16,
            color: 'yellow'
          },
          left: '1%'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            lineStyle: {
              color: '#57617B'
            }
          }
        },
        legend: {
          top: 20,
          icon: 'rect',
          itemWidth: 14,
          itemHeight: 5,
          itemGap: 13,
          data: ['喝水', '抽烟', '玩手机','疲劳驾驶'],
          right: '4%',
          textStyle: {
            fontSize: 12,
            color: '#F1F1F3'
          }
        },
        grid: {
          top: 100,
          left: '2%',
          right: '5%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          name:'分',
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: 'white'
            }
          },
          data: ['1', '2', '3', '3', '5', '6', '7', '8', '9', '10', '11', '12']
        }],
        yAxis: [{
          type: 'value',
          name: '次数',
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: 'white'
            }
          },
          axisLabel: {
            margin: 10,
            textStyle: {
              fontSize: 14
            }
          },
          splitLine: {
            lineStyle: {
              color: '#57617B'
            }
          }
        }],
        series: [{
          name: '喝水',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(137, 189, 27, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(137, 189, 27, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(137,189,27)',
              borderColor: 'rgba(137,189,2,0.27)',
              borderWidth: 12

            }
          },
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }, {
          name: '抽烟',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 136, 212, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(0, 136, 212, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(0,136,212)',
              borderColor: 'rgba(0,136,212,0.2)',
              borderWidth: 12

            }
          },
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }, {
          name: '玩手机',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(219, 50, 51, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(219, 50, 51, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(219,50,51)',
              borderColor: 'rgba(219,50,51,0.2)',
              borderWidth: 12
            }
          },
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        {
          name: '疲劳驾驶',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(219, 50, 51, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(219, 50, 51, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(129, 216, 207)',
              borderColor: 'rgba(129, 216, 207,0.2)',
              borderWidth: 12
            }
          },
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        ]
      }
    }
  },
  watch: {
    axisy: function(newVal, oldVal) {
      console.log(newVal, oldVal)
      this.chart.clear()
      console.log('重载')
      for(var i=0;i<4;i++)
      {
        this.lineOption.series[i].data = this.axisy[i]
      }
      this.lineOption.xAxis[0].data = this.axisx
      this.lineOption.xAxis[0].name = this.axisxtitle
      this.lineOption.title.show = this.emptyshow
      this.chart.setOption(this.lineOption, true)
    },
    titles: function(newVal, oldVal) {
      console.log(newVal, oldVal)
      this.chart.clear()
      this.lineOption.title.text = this.titles
      this.chart.setOption(this.lineOption, true)
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById(this.id))

      this.chart.setOption(this.lineOption)
    }
  }
}
</script>
