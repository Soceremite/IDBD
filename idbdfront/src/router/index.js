import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/',
    redirect:'/login'
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/autologin',
    component: () => import('@/views/login/autologin'),
    hidden: true
  },
  {
    path: '/register',
    component: () => import('@/views/register'),
    hidden: true
  },
  {
    path: '/dashboard',
    component: Layout,
    children: [{
      path: 'index',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '违规驾驶行为监测系统'}
    }]
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  }
]
export const asyncRoutes = [
  
  {
    path: '/detection',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'detection',
        component: () => import('@/views/detection/detect'),
        meta: { title: '驾驶监测', icon: 'monitor',roles:['user'] }
      }
    ]
  },
  {
    path: '/status',
    component: Layout,
    hidden: true,
    children: [
      {
        path: 'userstatus',
        name: 'userstatus',
        component: () => import('@/views/status/userstatus'),
        meta: { title: '驾驶员状态', icon: 'monitor',roles:['admin'] }
      }
    ]
  },
  {
    path: '/admin',
    component: Layout,
    children: [
      {
        path: 'usermanage',
        name: 'usermanage',
        component: () => import('@/views/admin/usermanage'),
        meta: { title: '用户信息', icon: 'user',roles:['admin'] }
      },
      {
        path: 'modifyuser',
        name: 'modifyuser',
        hidden: true,
        component: () => import('@/views/admin/modifyuser'),
        meta: { title: '用户修改', icon: 'user',roles:['admin'] }
      }
    ]
  },
  {
    path: '/illegal',
    component: Layout,
    children: [
      {
        path: 'mobile',
        name: 'Mobile',
        component: () => import('@/views/illegal/mobile'),
        meta: { title: '使用手机', icon: 'mobile',roles:['admin','user'] }
      }
    ]
  },
  {
    path: '/illegal',
    component: Layout,
    children: [
      {
        path: 'drink',
        name: 'Drink',
        component: () => import('@/views/illegal/drink'),
        meta: { title: '饮用饮料', icon: 'drink',roles:['admin','user']  }
      }
    ]
  },
  {
    path: '/illegal',
    component: Layout,
    children: [
      {
          path: 'smoke',
          name: 'smoke',
          component: () => import('@/views/illegal/smoke'),
          meta: { title: '违规吸烟', icon: 'smoke' , roles:['admin','user']  }
      }
    ]
  },
  {
    path: '/illegal',
    component: Layout,
    children: [
      {
        path: 'tired',
        name: 'tired',
        component: () => import('@/views/illegal/tired'),
        meta: { title: '疲劳驾驶', icon: 'tired' , roles:['admin','user']}
      }
    ]
  },
  {
    path: '/illegal',
    component: Layout,
    children: [
      {
        path: 'chart',
        name: 'userchart',
        hidden:true,
        component: () => import('@/views/illegal/chart'),
        meta: { title: '违规历史', icon: 'test' ,roles:['admin']}
      }
    ]
  },
  /*
  {
    path: '/illegal',
    component: Layout,
    redirect: '/illegal/chart',
    name: 'Illegal',
    meta: { title: '违规记录', icon: 'illegal',roles:['user','admin'] },
    children: [
      {
        path: 'chart',
        name: 'userchart',
        hidden:true,
        component: () => import('@/views/illegal/chart'),
        meta: { title: '违规历史', icon: 'test' }
      },
      {
        path: 'mobile',
        name: 'Mobile',
        component: () => import('@/views/illegal/mobile'),
        meta: { title: '使用手机', icon: 'mobile' }
      },
      {
        path: 'drink',
        name: 'Drink',
        component: () => import('@/views/illegal/drink'),
        meta: { title: '饮用饮料', icon: 'drink' }
      },
      {
        path: 'smoke',
        name: 'smoke',
        component: () => import('@/views/illegal/smoke'),
        meta: { title: '吸烟', icon: 'smoke' }
      },
      {
        path: 'tired',
        name: 'tired',
        component: () => import('@/views/illegal/tired'),
        meta: { title: '疲劳驾驶', icon: 'tired' }
      }
    ]
  },
  */
  {
    path: '/personal',
    component: Layout,
    redirect: '/personal/userinfo',
    name: 'Personal',
    meta: { title: '个人中心', icon: 'personal' ,roles:['user'] },
    children: [
      {
        path: 'userinfo',
        name: 'userinfo',
        component: () => import('@/views/personal/userinfo'),
        meta: { title: '个人信息', icon: 'userinfo'}
      },
    ]
  },
  /*
  {
    path: '代码链接',
    component: Layout,
    children: [
      {
        path: 'https://github.com/Soceremite/IDBD_Vue',
        meta: { title: '源码链接', icon: 'link',roles:['admin','user'] }
      }
    ]
  },
  */
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]
const createRouter = () => new Router({
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
