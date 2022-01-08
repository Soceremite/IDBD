<template>
    <div style="positon:relative">
        <div style="text-align:center;width:100%;position:absolute;top:50%;top:50%;transform:translate(0,-50%)">
            <div class="neu_content" style="border-radius: 50%;width:500px;height:500px;margin:auto">
                <video ref="video" width="500" height="500" style="border-radius:50%" autoplay></video>
            </div>
            <!--开启摄像头-->
            <button v-if="camera==false" class="neu_button " style="border-radius: 20%; width: 100px;margin:auto;margin-top:20px" @click.prevent="callCamera" >开启识别</button>
            <button v-else  class="neu_button " style="border-radius: 20%; width: 100px;margin:auto;margin-top:20px" @click.prevent="closeCamera" >关闭识别</button>
            <canvas   ref="canvas" width="500" height="500" style="position:fixed;left:100%;"></canvas>
        </div>
    </div>
</template>
<script>
import { MessageBox} from 'element-ui'
    export default {
        data () {
            return {
                timer:'',
                camera:false,
                suc:true
            }
        },
        methods: {
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

                }).catch(error => {
                    console.error('摄像头开启失败，请检查摄像头是否可用！')
                })
            },
            // 拍照
            photograph () {
                let ctx = this.$refs['canvas'].getContext('2d')
                // 把当前视频帧内容渲染到canvas上
                ctx.drawImage(this.$refs['video'], 0, 0, 500, 500)
                // 转base64格式、图片格式转换、图片质量压缩---支持两种格式image/jpeg+image/png
                let imgBase64 = this.$refs['canvas'].toDataURL('image/jpeg', 0.7)
                console.log('截取图片')
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
                this.camera=false;;
            },
            handle() {
                
                let that = this
                that.loading = true
                that.date1=new Date()
                
                if(that.camera == true  && that.suc == true)
                {
                    that.suc = false
                    this.$store.dispatch('user/autologin', this.photograph()).then(res=>{
                        this.closeCamera ()
                        that.suc = true
                        const {result} = res
                        console.log(res)
                        if(res.code == 200)
                        {
                            clearInterval(that.timer);
                            that.camera == false
                            MessageBox.confirm('用户'+result.user.username+'成功识别，是否登录？', {
                            confirmButtonText: 'Login',
                            cancelButtonText: 'Cancel',
                            type: 'warning'
                            }).then(() => {
                                this.$router.push({path:'/dashboard'})
                            },() =>{
                                this.callCamera ()
                            })
                        }
                    })
                }
                that.loading = false
                
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
