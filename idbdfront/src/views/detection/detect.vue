<template>
    <div class="app-container">
        <el-form ref="form">
            <div class="neu_content" style="width:642px;height:482px;margin:0 auto">
                <video ref="video" width="640" height="480" style="border-radius:10px" autoplay></video>
                <audio src="" controls="controls" ref="audio"  style="position:absolute;left:100%"></audio>
                <el-form-item style="margin-top:50px">
                <div style="margin:0 auto">
                    <button class="neu_button "   style="border-radius: 20%; width: 20%;margin:auto;margin-left:40%" @click.prevent="handleCamera" >
                        <span v-if="camera == false" >开启驾驶监测</span>
                        <span v-else>关闭驾驶监测</span>
                    </button>
                </div>
            </el-form-item>
            </div>
                <!--
                <div class="neu_content" style="float:left;width:642px;height:482px;margin-left:50px">
                   
                    <el-form style="height:50%">
                        <el-row>
                            <el-col :span="7" style="margin-left:3%">
                                <div class="neu_content" style="width:200px">
                                    <clock style="margin-top:20px;margin-left:30px;margin-bottom:20px"></clock>
                                    <div style="text-align:center">当前时间：{{date1.getHours()}}时{{date1.getMinutes(0)}}分</div>
                                </div>
                            </el-col>
                            <el-col :span="6" style="margin-left:5%">
                                <img :src="require('@/assets/'+avatar)" class="neu_content" style="width:150px;height:210px" alt="picture">
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
                -->
            
            <el-form-item>
                <!--canvas截取流(照片截图)-->
                <canvas   ref="canvas" width="640" height="480" style="position:absolute;marign-top:200px;left:150%"></canvas>
            </el-form-item>
            
            
            <!--确认-->
            <!--<el-button  type="primary" @click="photograph">拍照</el-button>-->
        </el-form>
    </div>
</template>
<script>
    import Clock from 'vue-clock2'
    import {mapGetters} from 'vuex'
    export default {
        components:{Clock},
        computed:{
            ...mapGetters([
            'userinfo',
            'avatar'
            ])
        },
        data () {
            return {
                date1:new Date(),
                timer:'',
                camera:false,
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
                audioplay:false
            }
        },
        methods: {
            handleCamera(){
                if(this.camera){
                    this.closeCamera()
                }
                else{
                    this.callCamera()
                }
            },
            // 调用摄像头
            callCamera () {
                // H5调用电脑摄像头API
                navigator.mediaDevices.getUserMedia({
                    video: true
                }).then(success => {
                    // 摄像头开启成功
                    this.$refs['video'].srcObject = success
                    // 实时拍照效果
                    this.$refs['video'].play()
                    this.camera=true;
                    this.audioplay=true
                    this.$refs.audio.src=require("@/assets/speech/welcome.wav")
                    this.$refs.audio.currentTime = 0;
                    this.$refs.audio.play();
                    this.audioplay=false
                }).catch(error => {
                    console.error('摄像头开启失败，请检查摄像头是否可用！')
                })
            },
            // 拍照
            photograph () {
                let ctx = this.$refs['canvas'].getContext('2d')
                // 把当前视频帧内容渲染到canvas上
                ctx.drawImage(this.$refs['video'], 0, 0, 640, 480)
                // 转base64格式、图片格式转换、图片质量压缩---支持两种格式image/jpeg+image/png
                let imgBase64 = this.$refs['canvas'].toDataURL('image/jpeg', 0.7)
                return imgBase64.replace(/^data:image\/\w+;base64,/, '')
 
            },
            // 关闭摄像头
            closeCamera () {
                if (!this.$refs['video'].srcObject) return
                let stream = this.$refs['video'].srcObject
                let tracks = stream.getTracks()
                tracks.forEach(track => {
                    track.stop()
                })
                this.camera=false;
                this.$refs['video'].srcObject = null
                this.audioplay=true
                this.$refs.audio.src=require("@/assets/speech/byebye.wav")
                this.$refs.audio.currentTime = 0;
                this.$refs.audio.play();
                this.audioplay=false
            },
            handle() {
                
                let that = this
                that.loading = true
                that.date1=new Date()
                if(that.camera == true && that.suc == true)
                {
                    that.suc = false
                    console.log('传输loading')
                    that.$store.dispatch('user/transportstream', that.photograph()).then(res => {
                        that.suc =true
                        res=JSON.parse(res)
                        let url=this.$refs.audio.src
                        if(res.status)
                        {
                            //that.Data.status=res.status
                            if(res.status=="疲劳")
                            url = require("@/assets/speech/perclos.wav")
                        }
                        if(res.smoke==1)
                        {
                            //that.Data.smoke='正在抽烟'
                            url = require("@/assets/speech/smoke.wav")
                        }
                        else
                        {
                            //that.Data.smoke='无'
                        }
                        if(res.drink==1)
                        {
                            //that.Data.drink='正在喝水'
                            url = require("@/assets/speech/drink.wav")
                            
                        }
                        else
                        {
                            //that.Data.drink='无'
                        }
                        if(res.phone==1)
                        {
                            //that.Data.phone='正在玩手机'
                            url = require("@/assets/speech/phone.wav")
                        }
                        else
                        {
                            that.Data.phone='无'
                        }
                        /*
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
                        */
                        if(that.$refs.audio.src!=url)
                        {
                            that.$refs.audio.src=url
                            if(that.audioplay == false)
                            {
                                that.audioplay = true
                                that.$refs.audio.currentTime = 0;
                                that.$refs.audio.play();
                                that.audioplay = false
                                
                            }
                            
                        }
                    }).catch(error =>{
                        that.$message.error({content:'处理失败'})
                        that.suc = true

                    })

                }
                that.loading = false
                
            },
            
        },
        mounted() {
            this.timer = setInterval(this.handle,30);
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
