<template>
  <div class="dashboard-container">
    <h1>驾驶员违规驾驶行为监测系统</h1>
    <h3>测试版本：v1.1.0</h3>
    <div class="dashboard-text">账号: {{ name }}</div>
    <!--
    <h2>蔡培彦</h2>
    <h3>代码：驾驶员的个人信息维护 包括修改个人信息 查看违规记录，以及前后端的Userinfo,Mobile,Drink,Tired,Yawn,Blink,Smoke模块</h3>
    <h3>文档：概要设计、测试报告、需求规格说明书（部分）</h3>
    <h2>刘亚东</h2>
    <h3>代码：数据集、模型训练（部分），总体代码设计，违规驾驶行为监测模块，包括针对前端传输数据，后端监测图片，针对违规行为记录到数据库，，管理员端实时显示和历史查看，css样式设计，测试修改</h3>
    <h3>文档：概要设计、需求规格说明书、使用说明书 （部分）</h3>
    <h2>王孜垚</h2>
    <h3>代码：整个管理员端口</h3>
    <h3>文档：概要设计、需求规格说明书（部分）</h3>
    <h2>陈宇静</h2>
    <h3>代码：数据集、模型训练（部分），人脸识别自动登录模块，以及没有完成不便展示的警察端口</h3>
    <h3>文档：概要设计、需求规格说明书（部分）</h3>
    <h2>未经允许不得商用</h2>
    -->
  </div>
  
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
