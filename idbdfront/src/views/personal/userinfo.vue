<template>
  <div class="app-container">
    <div class="neu_content" style="float:left;width:50%;height:100%">
      <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="昵称">
        <el-input v-model="form.nickName" />
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="form.realName" />
      </el-form-item>
      <el-form-item label="身份证号码">
        <el-input v-model="form.idcard" />
      </el-form-item>
      <el-form-item label="驾驶证号码">
        <el-input v-model="form.drivercard" />
      </el-form-item>
      <el-form-item label="车牌号码">
        <el-input v-model="form.carcard" />
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="form.sex" placeholder="请选择性别">
            <el-option
            v-for = "item in statusList"
            :key = "item.id"
            :label = "item.stauts_name"
            :value = "item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="出生日期">
        <el-col :span="11">
          <el-date-picker v-model="form.birth" type="date" placeholder="请选择生日日期" style="width: 40%;" />
        </el-col>
      </el-form-item>
      
      <el-form-item>
        <button class="neu_button" style="border-radius:20%;margin-left:25%;width:80px" type="primary" @click.prevent="handleUpdate">保存</button>
      </el-form-item>
    </el-form>
    </div>
    <div class="neu_content" style="float:left;width:40%;height:100%;margin-left:5%">
      <div style="positon:relative">
        <div style="text-align:center;width:50%;position:absolute;top:50%;transform:translate(0,-50%)">
          <!--
          <img :src="require('@/assets/'+avatar)" class="neu_content" style="width:150px;height:210px" alt="picture">
          -->
          <el-upload 
          class="upload-demo" 
          action="#" 
          accept="image/jpeg,image/gif,image/png"
          drag multiple 
          :auto-upload="false"
				  :file-list="fileList" 
          :on-change="handleChange">
					<i class="el-icon-upload"></i>
					<div class="el-upload__text">将图片拖到此处，或<em>点击上传</em></div>
					<div class="el-upload__tip" slot="tip">上传图片格式文件</div>
				</el-upload>
				<div slot="footer" class="dialog-footer">
					<button class="neu_button" style="border-radius:20%;width:80px" @click="dialogOfUpload = false">取 消</button>
					<button class="neu_button" style="border-radius:20%;width:80px;margin-left:10px" type="primary" @click="confirmUpload()">上 传</button>
				</div>
        </div>
          
      </div>
    </div>
    
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters([
      'userinfo',
      'avatar'
    ])
  },
  data() {
    return {
      dialogOfUpload: false,
			fileList: [],
      form:null,
      statusList:[{id:0,stauts_name:'未知'},{id:1,stauts_name:'男'},{id:2,stauts_name:'女'}]
    }
  },
  created() {
      this.form = this.userinfo
      console.log("userinfo"+this.form)
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    handleChange(file, fileList) { //文件数量改变
			this.fileList = fileList;
		},

		confirmUpload() { //确认上传
			var param = new FormData();
			this.fileList.forEach(
			  (val, index) => {
					param.append("file", val.raw);
					}
				);
			this.$store.dispatch('user/uploadimg', param).then(() => {
            this.$message.success({content:"修改成功"})
            this.loading = false
          }).catch(() => {
            this.$message.error({content:"上传失败"})
            this.loading = false
          })
		},
    handleUpdate() {
      //console.log("handleLogin")
      if(1){
          this.loading = true
          this.$store.dispatch('user/userinfoupdate', this.form).then(() => {
            this.$message.success({content:"修改成功"})
            //this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.$message.error({content:"修改失败"})
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      },
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
.el-form-item
{
    margin-bottom: 10px;
} 
.el-input >>> .el-input__inner {
  width:300px
}
</style>