<template>
  <div class="message-box animate_active">
    <div class="message-success" v-if="type === 'success'"><svg-icon icon-class="success" />{{ content }}</div>
    <div class="message-error" v-if="type === 'error'"><svg-icon icon-class="error" />{{ content }}</div>
  </div>
</template>
<script>
export default {
  name: 'Message',
  data() {
    return {
      type: '', // 接收一个参数，显示不同的消息框
      content: '', // 将要显示消息内容
      duration: 2000 // 消息框显示时间
    }
  },
  mounted() {
  	// 消息框定时隐藏
    setTimeout(() => {
      // 隐藏时卸载掉dom
      this.$destroy(true)
      this.$el.parentNode.removeChild(this.$el)
    }, this.duration)
  }
}
</script>

<style scoped lang='less'>
.down{
    &-enter{
        &-from{
            transform:translate3d(0,-75px,0);
            opacity: 0;
        } 
        &-active{
            transition:all 0.5s;
        }
        &-to{
            transform:none;
            opacity: 1;
        }
    }
}

/* 消息框的样式，采用fixed定位 */
.message-box {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 10px;
  left: 50%;
  right: 0;
  z-index: 9999;
  width: 300px;
  height: 30px;;
  margin-left: -150px;
  background:#ecf0f3;
  border-radius: 10px;
  padding: 30px 10px;
  box-shadow:-5px -5px 20px #fff, 5px 5px 20px #babecc;
}
.message-success{
    color:rgb(0, 99, 21);
}
.message-error{
    color:rgb(252, 1, 1);
}
</style>