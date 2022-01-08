<template>
    <div class="app-container">
        <el-form ref="form">
            <div class="neu_content" style="width:642px;height:482px;margin:0 auto">        
                <el-form style="height:50%">
                        <el-row>
                            <el-col :span="7" style="margin-left:3%">
                                <div class="neu_content" style="width:200px">
                                    <clock style="margin-top:20px;margin-left:30px;margin-bottom:20px"></clock>
                                    <div style="text-align:center">当前时间：{{date1.getHours()}}时{{date1.getMinutes(0)}}分</div>
                                </div>
                            </el-col>
                            <el-col :span="6" style="margin-left:5%">
                                <img :src="require('@/assets/'+userinfo.face)" class="neu_content" style="width:150px;height:210px" alt="picture">
                            </el-col>
                            <el-col :span="8" style="margin-left:2%;margin-right:2%">
                                <el-row>
                                    <el-form-item style="margin-bottom:0px" class="special-label" label="姓  名" label-width="60px">
                                        <el-input style="width:100%" :disabled="true" v-model="userinfo.realName"></el-input>
                                    </el-form-item>
                                </el-row>
                                <el-row>
                                    <el-form-item style="margin-bottom:0px" class="special-label" label="身份证号" >
                                        <el-input style="width:100%" :disabled="true" v-model="userinfo.idcard"></el-input>
                                    </el-form-item>
                                </el-row>
                                <el-row>
                                    <el-form-item style="margin-bottom:0px" class="special-label" label="车牌号码" >
                                        <el-input style="width:100%" :disabled="true" v-model="userinfo.carcard"></el-input>
                                    </el-form-item>
                                </el-row>
                            </el-col>
                        </el-row>
                    </el-form>
                    <el-form ref="form" style="text-align:center;display:left" label-width="60px" :model="Data">
                        <el-row>
                            <el-form-item style="margin-bottom:0px"  prop="status" label="状态">
                                <el-input v-if="(Data.status==='清醒')"   style="width:100px" :disabled="true" v-model="Data.status"></el-input> 
                                <el-input v-else class="rt-input"  style="width:100px" :disabled="true" v-model="Data.status"></el-input>
                            </el-form-item>
                        </el-row>
                        <el-row>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="抽烟">
                                    <el-input v-if="(Data.smoke==='无')"   style="width:100px" :disabled="true" v-model="Data.smoke"></el-input> 
                                    <el-input v-else class="rt-input"  style="width:100px" :disabled="true" v-model="Data.smoke"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="喝水">
                                    <el-input v-if="(Data.drink==='无')"   style="width:100px" :disabled="true" v-model="Data.drink"></el-input> 
                                    <el-input v-else class="rt-input"  style="width:100px" :disabled="true" v-model="Data.drink"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="玩手机">
                                    <el-input v-if="(Data.phone==='无')"   style="width:100px" :disabled="true" v-model="Data.phone"></el-input> 
                                    <el-input v-else class="rt-input"  style="width:100px" :disabled="true" v-model="Data.phone"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="打哈欠">
                                    <el-input style="width:100px" :disabled="true" v-model="Data.yawn"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="眨眼">
                                    <el-input style="width:100px" :disabled="true" v-model="Data.eye"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item style="margin-bottom:0px" label="Perclos">
                                    <el-input style="width:100px" :disabled="true" v-model="Data.perclos"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </div>
        </el-form>
    </div>
</template>
<script>
    import Clock from 'vue-clock2'
    export default {
        components:{Clock},
        data () {
            return {
                date1:new Date(),
                timer:'',
                suc:true,
                Data:{
                    status:'清醒',
                    smoke:'无',
                    drink:'无',
                    phone:'无',
                    eye:0,
                    yawn:0,
                    perclos:0
                },
                colorstatus:'red',
                userinfo:[]
            }
        },
        created() {
            this.$store.dispatch('user/admingetUserInfo',this.$route.params.userid).then(res => {
                console.log(res)
                this.userinfo = res
            }).catch(error =>{
                this.$message.error({content:error})
                })
        },
        methods: {
            handle() {
                let that = this
                that.date1=new Date()
                if(that.suc == true)
                {
                    that.suc = false
                    that.$store.dispatch('user/getstatus',this.$route.params.userid).then(response => {
                        console.log("res"+typeof response)
                        var res=typeof arg=='string'?JSON.parse(response):response
                        //const res=JSON.parse(response)
                        that.suc = false
                        that.loading = true
                        if(res.status)
                        {
                            that.Data.status=res.status
                        }
                        if(res.smoke==1)
                        {
                            that.Data.smoke='正在抽烟'
                        }
                        else
                        {
                            that.Data.smoke='无'
                        }
                        if(res.drink==1)
                        {
                            that.Data.drink='正在喝水'
                            
                        }
                        else
                        {
                            that.Data.drink='无'
                        }
                        if(res.phone==1)
                        {
                            that.Data.phone='正在玩手机'
                        }
                        else
                        {
                            that.Data.phone='无'
                        }
                        
                        if(res.yawn)
                        {
                            that.Data.yawn=res.yawn
                        }
                        if(res.eye)
                        {
                            that.Data.eye=res.eye
                        }
                        if(res.perclos)
                        {
                            that.Data.perclos=res.perclos
                        }
                        that.loading = false
                        that.suc =true
                    }).catch(error =>{
                        console.log(error)
                        this.$message.error({content:'用户可能没有正在使用监测系统'})
                        that.suc =true
                        clearInterval(this.timer);
                    })

                }
                
                
            },
            
        },
        mounted() {
            this.timer = setInterval(this.handle,100);
        },
        beforeDestory(){
            clearInterval(this.timer);
        }
    }

</script>
<style  scoped>
.el-input{
    margin:left
}
.el-form-item
{
    margin-bottom: 0px;
} 
.el-form-item >>> .el-form-item__label{
    text-align:left
}
.special-label >>> .el-form-item__label{
    text-align:center;
    margin-bottom: 0px;
}
.el-input >>> .el-input__inner {
  color: black !important;
  cursor: pointer;
  text-align: center;
}
.rt-input >>> .el-input__inner {
  color: red !important;
  cursor: pointer;
  text-align: center;
}
</style>
