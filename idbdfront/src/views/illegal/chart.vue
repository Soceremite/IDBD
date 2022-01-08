<template>
<el-form>
  <el-row class="date-container">
    <el-col :span="7">
      <el-form-item label="日期" prop="startDate">
        <el-date-picker v-model="addDrillRecordRow.startDate" class="baseInput" type="date" placeholder="选择日期" format="yyyy 年 MM 月 dd 日" :picker-options="pickerOptionsStart">
      </el-date-picker></el-form-item>
    </el-col>
    <el-col :offset="1" :span="11">
      <el-form-item label="时间段选择" prop="time" >
        <el-time-picker is-range v-model="addDrillRecordRow.Time" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" placeholder="选择时间范围"> </el-time-picker>
      </el-form-item>
    </el-col>
    <el-col :offset="2" :span="2">
      <button class="neu_button "   style="margin-top:35px;border-radius: 20%; width: 100px;" @click.prevent="handle" >确定</button>
    </el-col>
  </el-row>
  <el-row class="chart-container">
     <chart height="92%" width="100%" :axisx="axisx" :axisxtitle='axisxtitle' :axisy="axisy" :emptyshow="emptyShow" :titles="titles" />
  </el-row>
  <el-row>
        <div class="chart-wrapper">
          <pie-chart  :piechartdata="piechartdata"/>
        </div>
    </el-row>
  </el-form>
</template>

<script>
import Chart from '@/components/Charts/LineMarker'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'
export default {
  name: 'userchart',
  components: { 
    Chart,
    RaddarChart,
    PieChart,
    BarChart,
     },
  data(){
    return{
      addDrillRecordRow:{
        startDate:new Date(),
        Time:[new Date(new Date().getTime() - 3600 * 1000 * 1),new Date()]
      },
      pickerOptionsStart: {
        disabledDate: time => {
          if (this.addDrillRecordRow.startDate) {
            return (
              time.getTime() > Date.now() - 8.64e6 ||
              time.getTime() > this.addDrillRecordRow.startDate  
            );
          }
          return time.getTime() > Date.now() - 8.64e6; /*今天及之前，注意数字不一样*/
        }
      },
      titles:'驾驶员历史违规记录',
      axisx: [],
      axisxtitle:'分',
      axisy: [], // 画图的y轴
      emptyShow: true, // 定义是否已经可以渲染
      sortValue: '', // 排序条件选择
      noneTitle: '测试', // 选择查看的图表没有数据
      split:30,
      unit:'second',
      piechartdata:[0,0,0,0]
    }
  },
  created() {
    this.getCharts()
  },
  methods:{
    choosetimeperiod(start_time,end_time){
      var res = this.split;
      var st = new Date(start_time)
      var total = (new Date(end_time).getTime()-st.getTime())/1000
      var day = parseInt(total / (24*60*60));//计算整数天数
      var afterDay = total - day*24*60*60;//取得算出天数后剩余的秒数
      var hour = parseInt(afterDay/(60*60));//计算整数小时数
      var afterHour = total - day*24*60*60 - hour*60*60;//取得算出小时数后剩余的秒数
      var min = parseInt(afterHour/60);//计算整数分
      var second = total - day*24*60*60 - hour*60*60 - min*60;//取得算出分后剩余的秒数
      console.log(total+'秒：'+day+'天'+hour+'时'+min+'分'+second+'秒')
      this.unit = 'second'
      this.axisxtitle='分'
      if(hour>=6)//长于6小时按小时分割
      {
        res = hour
        this.unit='hour'
        this.axisxtitle='小时'

      }
      else if(hour>1)
      {
        res = (hour*60+min)/10
        this.unit= 'minute'
        this.axisxtitle='10分钟'
      }
      else if (min<=1)
      {
        this.axisxtitle='秒'
      }
      console.log('res'+res+'unit'+this.unit)
      return res
    },
    datestr(date,time,sign){
      if (!sign)
      {
        sign='-'
      }
      let year= date.getFullYear(),
      month= date.getMonth()+1,
      day= date.getDate()
      let hours =time.getHours(),
      minutes = time.getMinutes(),
      seconds =time.getSeconds()
      return (
        year +
        sign +
        this.mendZero(month) +
        sign +
        this.mendZero(day) +
        ' ' +
        this.mendZero(hours) +
        ':' +
        this.mendZero(minutes) +
        ':' +
        this.mendZero(seconds)
      )
    },
    mendZero(num) {
      return (num = num < 10 ? '0' + num : num)
    },
    getCharts(){
      let start_time = this.datestr(this.addDrillRecordRow.startDate,this.addDrillRecordRow.Time[0],'-')
      let end_time = this.datestr(this.addDrillRecordRow.startDate,this.addDrillRecordRow.Time[1],'-')
      this.split = this.choosetimeperiod(start_time,end_time)
      console.log(start_time+end_time)
      let data = {userid:this.$route.params.userid,start_time:start_time,end_time:end_time,split:this.split,unit:this.unit}
      this.$store.dispatch('user/getillegaldata', data).then(res => {
        const{axisx,drink,mobile,smoke,tired,piechartdata} =res
        this.axisy=[]
        this.axisy.push(drink)
        this.axisy.push(smoke)
        this.axisy.push(mobile)
        this.axisy.push(tired)
        this.axisx=axisx
        this.piechartdata=piechartdata
        console.log(this.axisy)
      }).catch(error=>{
        console.log(error)
      }
      )
    },
    handle(){
      this.getCharts()
    }
  },

}
</script>

<style scoped>
.chart-container{
  position: relative;
  width: 80%;
  margin-left:10%;
  /*height: calc(100vh - 250px);*/
  height:500px
}
.date-container{
  position: relative;
  width: 80%;
  margin-left:10%;
}
.el-form-item >>> .el-form-item__label{
    text-align:left;
    margin-bottom: 0px;
}
.chart-wrapper{
  margin:0 auto;
}
</style>

