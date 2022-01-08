<template>
  <div class="ice-layout ice-blank-layout">
    <div class="login-page">
      <div class="user-login">
        <div class="login-bg" />
        <div class="login-main">
          <div class="neu_text" style="font-size: 5em;text-align:center">
              欢迎来到
              <br/>
              驾驶员违规驾驶行为监测系统
          </div>

          <div class="login-content neu_content" style="width:300px;min-width:300px;padding:40px 30px">
              <div class="neu-shadow-ring-2 item" style="width:100px;height:100px;margin:auto"> </div>
            <el-form
              :model="loginForm"
              :rules="loginRules"
              ref="loginForm"
              @submit.native.prevent
              >
              <el-form-item prop="username">
                <input
                  v-model="loginForm.username"
                  auto-complete="off"
                  clearable
                  placeholder="用户名"
                  class="neu_input"
                  autocomplete
                />
              </el-form-item>
              <el-form-item prop="password">
                <input
                type="password"
                  v-model="loginForm.password"
                  auto-complete="new-password"
                  clearable
                  placeholder="密码"
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
              @click.prevent="handleLogin"
              >登录</button>
              </form>
              <form class="segment">
                <button class="neu_button unit" type="button" @click="$router.back(-1)"><svg-icon icon-class="Back" /></button>
                <button class="neu_button unit" type="button" @click="autoLoginClick"><svg-icon icon-class="face" /> </button>
                <button class="neu_button unit" type="button" @click="hrefClick"><svg-icon icon-class="Register" /> </button>
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

  name: 'AdminLogin',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length<1) {
        callback(new Error('Please enter the correct user name'))
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
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
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
    handleLogin() {
      //console.log("handleLogin")
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(res => {
            console.log(res)
            this.$message.success({content:res})
            this.$router.push({ path: this.redirect || '/dashboard' })
            this.loading = false
          }).catch(error => {
            this.$message.error({content:res || error})
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    hrefClick(){
      this.$router.push({path:'/register'})
    },
    autoLoginClick(){
      this.$router.push({path:'/autologin'})
    }
  }
}
</script>

<style lang="scss">
.ice-layout {
  -webkit-box-direction: normal;
}
.user-login {
  position: relative;
  height: 100vh;
  .login-bg {
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    background-size: cover;
    background-color: #ecf0f3;
  }
  .login-main {
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
  .login-left-title {
    text-align: center;
    font-size: 36px;
    letter-spacing: 2px;
    line-height: 48px;
  }
  .login-content {
    margin-top:100px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    
    .login-title {
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