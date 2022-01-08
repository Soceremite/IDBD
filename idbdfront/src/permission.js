import router, { resetRouter } from './router'
import store from './store'
import Message from '@/components/Message/Message'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'
import Router from 'vue-router'
NProgress.configure({ showSpinner: false }) // NProgress Configuration

const whiteList = ['/login','/autologin','/register'] // no redirect whitelist

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()
  console.log("from:"+from.path+"\n"+"to:"+to.path)
  if((to.path === '/login'))
  {
    next()
  }
  else if (hasToken) {
    console.log('hasGetToken:'+getToken())
    if (whiteList.indexOf(to.path) !== -1) {
      // if is logged in, redirect to the home page
      next({ path: '/dashboard/index' })
      NProgress.done()
    } else {
      //console.log(store.getters.roles)
      const accessRoutes = await store.dispatch('permission/generateRoutes',store.getters.roles)
      //console.log(accessRoutes)
      router.options.routes = store.getters.permission_routes
      //console.log(router.options.routes)
      resetRouter()
      router.addRoutes(accessRoutes)
      //console.log('addroute success')
      const hasuserinfo = store.getters.name 
      //console.log('hasGetInfo:'+hasGetInfo)
      if (hasuserinfo) {
        next()
      } else {
        try {
          // get user info
          await store.dispatch('user/getUserInfo')
          next({ ...to, replace: true })
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          console.log(error)
          Message.error({content:'无法授权'})
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token*/
    //console.log('hasGetToken: noToken')
    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      // get user info
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
