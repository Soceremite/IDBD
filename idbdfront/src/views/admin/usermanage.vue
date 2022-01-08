<template>
    <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px" >
      <el-table :data="form" height="600" 
      :header-cell-style="{'text-align':'center'}"
      :cell-style="{'text-align':'center'}" 
      style="width: 900px;margin:0 auto"
      class="my-table">
        <el-table-column
        prop="id"
        type="index"
        label="用户号"
        width="100">
        </el-table-column>
        <el-table-column
        prop="username"
        label="用户名"
        width="100"
        >
        </el-table-column>
        <el-table-column
        prop="create_time"
        label="创建时间"
        width="300"
        >
        </el-table-column>
        <el-table-column
        prop="#"
        label="操作"
        width="400"
        >
        <template slot-scope="scope">
          <el-button type="primary" @click="viewuserstatus(scope.row)">实时状态</el-button>
          <el-button type="primary" @click="viewuserhistory(scope.row)">历史状态</el-button>
          <el-button type="primary" @click="modifyuser(scope.row)">修改</el-button>
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
export default {
  data() {
    return {
      form:[],
      newid:null
    }
  },
  created() {
    console.log('loading')
    this.$store.dispatch('user/admingetuser').then(data => {
      console.log(data)
      this.loading = true 
      if(data.User!=null)
      {
        this.form = data.User
        console.log("User"+data.User)
      }
      this.$message.success({content:data.msg}) 
      this.loading = false
      }).catch(error => {
        this.loading = false
        this.$message.error({content:error})
      }
    ) 
  },
  methods: {
      modifyuser(v){
        this.$router.push({ name:'modifyuser', params: { userid: v.id }})
      },
      viewuserstatus(v){
        this.$router.push({ name:'userstatus', params: { userid: v.id }})
      },
      viewuserhistory(v){
        this.$router.push({ name:'userchart', params: { userid: v.id }})
      },
      deleteuser(v){
          console.log(v.id)
          this.newid=this.form.findIndex((item)=>{
            return item.id==v.id;
        })
        this.loading = true
        this.$store.dispatch('user/admindeleteuser',v.id).then(data => {
            this.$message.success({content:data.msg}) 
            this.form.splice(this.newid,1); 
            this.loading = false
        }).catch(error => {
        this.loading = false
        this.$message.error({content:error})
      }
      )
   }
}}
</script>