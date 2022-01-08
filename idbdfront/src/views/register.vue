<template>
  <div class="ice-layout ice-blank-layout">
    <div class="register-page">
      <div class="user-register">
        <div class="register-bg" />
        <div class="register-main">
          <div class="neu_text" style="font-size: 5em;text-align:center">
              欢迎来到
              <br/>
              驾驶员违规驾驶行为监测系统
          </div>

          <div class="register-content neu_content" style="width:300px;min-width:300px;padding:40px 30px">
              <div class="neu-shadow-ring-2 item" style="width:100px;height:100px;margin:auto"> </div>
            <el-form
              :model="registerForm"
              :rules="registerRules"
              ref="registerForm"
              @submit.native.prevent
              >
              <el-form-item prop="username">
                <input
                  v-model="registerForm.username"
                  auto-complete="off"
                  clearable
                  placeholder="用户名"
                  class="neu_input"
                  autocomplete
                />
              </el-form-item>
              <el-form-item prop="password1">
                <input
                type="password"
                  v-model="registerForm.password1"
                  auto-complete="new-password"
                  clearable
                  placeholder="密码"
                  class="neu_input"
                  autocomplete
                />
              </el-form-item>
              <el-form-item prop="password2">
                <input
                type="password"
                  v-model="registerForm.password2"
                  auto-complete="new-password"
                  clearable
                  placeholder="确认密码"
                  class="neu_input"
                  autocomplete
                />
              </el-form-item>
              <form>
              <button
              class="neu_button red"
              style="border-radius: 320px; width: 30%;margin:auto"
              type="primary"
              native-type="submit"
              @click.prevent="handleregister"
              >注册</button>
              </form>
              <form class="segment">
                <button class="neu_button unit" type="button" @click="$router.back(-1)"><svg-icon icon-class="Back" /></button>
                <router-link to="Index">
                <button class="neu_button unit" type="button"><svg-icon icon-class="home" /> </button>
                </router-link>
                <button class="neu_button unit" type="button" @click="hrefClick"><svg-icon icon-class="github" /> </button>
              </form>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'
export default {

  name: 'register',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length<1) {
        callback(new Error('Please enter the username'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 4) {
        callback(new Error('The password can not be less than 4 digits'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {
        username: '',
        password1: '',
        password2:''
      },
      registerRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password1: [{ required: true, trigger: 'blur', validator: validatePassword }],
        password2: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleregister() {
      //console.log("handleregister")
      this.$refs.registerForm.validate(valid => {
        if (valid) {
            if(this.registerForm.password1!==this.registerForm.password2)
            {
                this.$message.error({content:"两次密码不一致"})
                return false
            }
          this.loading = true
          this.$store.dispatch('user/register', this.registerForm).then(res => {
            this.$message.success({content:res})
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    hrefClick(){
      window.open("https://github.com/Soceremite/IDBD_Vue")
    },
    indexClick(){
      this.$router.push({path:'/login'})
    },
    dashboardClick(){
      this.$router.push({path:'/dashboard'})
    }
  }
}
</script>

<style lang="scss">
.ice-layout {
  -webkit-box-direction: normal;
}
.user-register {
  position: relative;
  height: 100vh;
  .register-bg {
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    background-size: cover;
    background-color: #ecf0f3;
  }
  .register-main {
    position: absolute;
    top: -100px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    max-width: 1080px;
    margin: 0px auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  .register-left-title {
    text-align: center;
    font-size: 36px;
    letter-spacing: 2px;
    line-height: 48px;
  }
  .register-content {
    margin-top:100px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    
    .register-title {
      margin: 0px 0px 20px;
      text-align: center;
      color: #5a84a2;
      letter-spacing: 12px;
    }

  }
}


form {
  padding: 16px 0px 16px 0px;
  width: 100%;
  margin: 0 auto;
}

.segment {
  padding: 32px 0;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 24px;
  width: 100%;
}

input {
  margin-right: 8px;
  box-shadow: inset 2px 2px 5px #BABECC, inset -5px -5px 10px #FFF;
  width: 100%;
  box-sizing: border-box;
  transition: all 0.2s ease-in-out;
  appearance: none;
  -webkit-appearance: none;
}
input:focus {
  box-shadow: inset 1px 1px 2px #BABECC, inset -1px -1px 2px #FFF;
}


.input-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.input-group label {
  margin: 0;
  flex: 1;
}
</style>