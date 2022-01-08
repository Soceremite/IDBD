import { login,autologin,register,admingetuser,transportstream,logout, getUserInfo,userinfoupdate,getusermobile,getuserdrink,getusertired,getuseryawn,getuserblink,getusersmoke,admindeleteuser,admingetUserInfo,deletedrink,deletemobile,deletesmoke,deletetired,fileupload,getstatus,getillegaldata } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'
const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    user: {},
    avatar: '',
    userinfo:{},
    roles:[]
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_USER: (state, user) => {
    state.user = user
  },
  SET_USERINFO: (state, userinfo) => {
    state.userinfo = userinfo
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
}

const actions = {

  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password}).then(response => {
        //console.log('响应登录')
        const {result,roles,msg} = response
        commit('SET_TOKEN', result.accessToken.token)
        setToken(result.accessToken.token)
        commit('SET_ROLES',roles)
        commit('SET_USER', result.user)
        if(roles.includes('admin'))
        {
          commit('SET_NAME', result.user.adminname)
          commit('SET_AVATAR', result.user.face)
          
        }      
        //console.log(result.accessToken.token)
        //commit('SET_NAME',res.user.username)
        resolve(msg)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // user autologin
  autologin({ commit }, stream) {
    return new Promise((resolve, reject) => {
      autologin({photo:stream }).then(response => {
        const res = response.result
        console.log(res)
        commit('SET_TOKEN', res.accessToken.token)
        setToken(res.accessToken.token)
        commit('SET_USER', res.user)
        commit('SET_ROLES',response.roles)
        //commit('SET_NAME',res.user.username)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // user register
  register({ commit }, userInfo) {
    const { username, password1 } = userInfo
    return new Promise((resolve, reject) => {
      register({ username: username.trim(), password: password1}).then(response => {
        //commit('SET_NAME',res.user.username)
        resolve(response.msg)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // user info
  getUserInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUserInfo({viewUserUuid: state.user.id }).then(response => {
        const { result } = response
        if (!result) {
          return reject('getuserinfo error')
        }
        const { nickName, face } = result.userinfo
        commit('SET_USERINFO',result.userinfo)
        commit('SET_NAME', nickName)
        commit('SET_AVATAR', face)
        resolve(response.msg)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // admin get user info
  admingetUserInfo({ commit, state },userid) {
    return new Promise((resolve, reject) => {
      getUserInfo({viewUserUuid: userid }).then(response => {
        const { result } = response
        if (!result) {
          return reject('admin getuserinfo error')
        }
        resolve(result.userinfo)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // admin get user status
  getstatus({ commit, state },userid) {
    return new Promise((resolve, reject) => {
      getstatus({viewUserUuid: userid }).then(response => {
        const { result } =response
        if (!result) {
          return reject('getuserstatus error')
        }
        resolve(result)
      }).catch(error => {
        reject(error)
      })
    })
  },
  getillegaldata({ commit, state },data) {
    return new Promise((resolve, reject) => {
      getillegaldata(data).then(response => {
        const { result } =response
        if (!result) {
          return reject('getuserstatus error')
        }
        resolve(result)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // get image solution
  transportstream({ commit},stream) {
    return new Promise((resolve, reject) => {
      transportstream({photo:stream,userid: state.user.id }).then(response => {
        const { data } = response
        if (!data) {
          return reject('failed')
        }
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      let roles = 'user'
      if (state.roles.includes('admin'))
      {
        roles='admin'
      }

      logout({token:state.token,roles:roles}).then(response => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve(response.msg)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // update userinfo
  userinfoupdate({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      userinfoupdate({ userid:state.user.id,userinfo:userInfo}).then(response => {
        const res = response.userinfo
        //setToken(res.accessToken.token) cookie
        commit('SET_USERINFO', res)
        const { nickName, face } = res
        commit('SET_NAME', nickName)
        commit('SET_AVATAR', face)
        //commit('SET_NAME',res.user.username)
        resolve(response.msg)
      }).catch(error => {
        reject(error)
      })
    })
  },
 // update userinfo
 adminuserinfoupdate({ commit },data) {
  return new Promise((resolve, reject) => {
    console.log(data)
    userinfoupdate({ userid:data.userid,userinfo:data.data}).then(response => {
      const res = response.userinfo
      resolve(response.msg)
    }).catch(error => {
      reject(error)
    })
  })
},
admingetuser({ commit, state }) {
  return new Promise((resolve, reject) => {
    admingetuser().then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},

admindeleteuser({ commit, state },uid) {
  return new Promise((resolve, reject) => {
    admindeleteuser({userid:uid}).then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},
// user info
admingetUserInfo({ commit, state },userid) {
  return new Promise((resolve, reject) => {
    console.log(userid)
    admingetUserInfo({viewUserUuid: userid }).then(response => {
      const { result } = response
      console.log(result)  
      if (!result.userinfo) {
          return reject('failed')
        }
        resolve(result.userinfo)
    }).catch(error => {
      reject(error)
    })
  })
},

//upload file
// update userinfo
uploadimg({ commit }, img) {
  return new Promise((resolve, reject) => {
    uploadimg({ userid:state.user.id,img:img}).then(response => {
      resolve(response.msg)
    }).catch(error => {
      reject(error)
    })
  })
},
//get user mobile
getusermobile({ commit, state },search=null) {
  return new Promise((resolve, reject) => {
    if(state.roles.includes('admin'))//管理员
    {
      getusermobile({viewUserUuid: 0,search:search }).then(response => {
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }
    else //普通用户
    {
      getusermobile({viewUserUuid: state.user.id,search:search }).then(response => {
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }  
  })
},

//get user drink
getuserdrink({ commit, state },search=null) {
  return new Promise((resolve, reject) => {
    if(state.roles.includes('admin'))
    {
      getuserdrink({viewUserUuid: 0,search:search }).then(response => {
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }
    else
    {
      getuserdrink({viewUserUuid: state.user.id,search:search }).then(response => {
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }  
  })
},
//get user tired
getusertired({ commit, state },search=null) {
  return new Promise((resolve, reject) => {
    if(state.roles.includes('admin'))
    {
      getusertired({viewUserUuid: 0,search:search }).then(response => {
        //commit('SET_MOBILE',res)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }
    else
    {
      getusertired({viewUserUuid: state.user.id,search:search }).then(response => {
        //commit('SET_MOBILE',res)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    }    
  })
},

//get user smoke
getusersmoke({ commit, state },search=null) {
return new Promise((resolve, reject) => {
  if(state.roles.includes('admin'))
  {
    getusersmoke({viewUserUuid: 0,search:search }).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  }
  else
  {
    getusersmoke({viewUserUuid: state.user.id,search:search }).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
  })
  }
  
})
},
//delete user drink
deletedrink({ commit, state },iid) {
  return new Promise((resolve, reject) => {
    deletedrink({id:iid}).then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},
//delete user mobile
deletemobile({ commit, state },iid) {
  return new Promise((resolve, reject) => {
    deletemobile({id:iid}).then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},
//delete user smoke
deletesmoke({ commit, state },iid) {
  return new Promise((resolve, reject) => {
    deletesmoke({id:iid}).then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},
//delete user tired
deletetired({ commit, state },iid) {
  return new Promise((resolve, reject) => {
    deletetired({id:iid}).then(response => {
      console.log(response)
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
},
  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

