<template>
  <div class="dashboard-container">
    <h1>驾驶员违规驾驶行为监测系统</h1>
    <h3>测试版本：v1.1.0</h3>
    <div class="dashboard-text">账号: {{ name }}</div>
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
