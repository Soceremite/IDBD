<template>
    <div class="app-container">
      <div v-if="roles.includes('admin')" style="width: 900px;margin:0 auto">
      <el-row>
        <el-col :span="5">
          <el-input  v-model="search.userid" placeholder="请输入用户号" style="width:120px;margin:0 auto"></el-input>
        </el-col>
        <el-col :span="7">
          <el-date-picker v-model="search.start_time" type="datetime" placeholder="选择起始时间" :picker-options="startPickerOptions"></el-date-picker>
        </el-col>
        <el-col :span="7">
          <el-date-picker v-model="search.end_time" type="datetime" placeholder="选择终止时间"></el-date-picker>
        </el-col>
        <el-col :span="4">
          <button class="neu_button" style="border-radius:20%;margin-left:30px" @click="handleClick">搜索</button>
        </el-col>
      </el-row>
    </div>
    <el-form ref="form" :model="form" label-width="120px">
      <el-table :data="form" height="600" 
      :header-cell-style="{'text-align':'center'}"
      :cell-style="{'text-align':'center'}" 
      style="width: 900px;margin:0 auto"
      class="my-table">
        <el-table-column
        prop="user"
        label="用户号"
        width="100">
        </el-table-column>
        <el-table-column
        prop="start_time"
        label="起始时间"
        width="360"
        >
        </el-table-column>
        <el-table-column
        prop="end_time"
        label="终止时间"
        >
        </el-table-column>
         <el-table-column
         v-if="roles.includes('admin')"
        prop=""
        label="操作"
        >
        <template  slot-scope="scope">
                <el-button type="danger" @click="deleteuser(scope.row)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    </el-form>
  </div>
  
</template>
<style scoped>
.my-table{
  margin-left:calc(100%-900px)
}
</style>
<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  data() {
    return {
      search:{
        userid:null,
        start_time:null,
        end_time:new Date()
      },
      startPickerOptions:{
        disabledDate: (time) => {
          //小于最小时间或者大于最大时间都不可选
            return time > this.search.end_time 
          }
      },
      form:null
    }
  },
  created() {
    this.handleClick()
  },
  methods: {
    deleteuser(v){
          console.log(v.id)
          this.newid=this.form.findIndex((item)=>{
            return item.id==v.id;
        })
        this.loading = true
        this.$store.dispatch('user/deletesmoke',v.id).then(data => {
            this.$message.success({content:data.msg}) 
            this.form.splice(this.newid,1); 
            this.loading = false
        }).catch(error => {
        this.loading = false
        this.$message.error({content:error})
      })
     },
      //日期转字符串格式
    DateToStr(date) {
      if(date)
      {
        var year = date.getFullYear();//年
        var month = date.getMonth();//月
        var day = date.getDate();//日
        var hours = date.getHours();//时
        var min = date.getMinutes();//分
        var second = date.getSeconds();//秒
        return year + "-" +
          ((month + 1) > 9 ? (month + 1) : "0" + (month + 1)) + "-" +
          (day > 9 ? day : ("0" + day)) + " " +
          (hours > 9 ? hours : ("0" + hours)) + ":" +
          (min > 9 ? min : ("0" + min)) + ":" +
          (second > 9 ? second : ("0" + second));
      }
      return null
    },
     handleClick(){
       var searchdata = {userid:this.search.userid,start_time:this.DateToStr(this.search.start_time),end_time:this.DateToStr(this.search.end_time)}
        this.$store.dispatch('user/getusersmoke',searchdata).then(data => {
          console.log(data)
          this.loading = true
          if(data)
          {
            this.form = data.smoke
          }
          this.$message.success({content:data.msg}) 
          this.loading = false
        }).catch(error => {
          this.loading = false
          this.$message.error({content:data.msg||error})
        }
      )
    }
  }
}
</script>