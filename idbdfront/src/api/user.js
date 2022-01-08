import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login/',
    method: 'post',
    data
  })
}

export function autologin(data) {
  return request({
    url: '/user/autologin/',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: '/user/register/',
    method: 'post',
    data
  })
}

export function getUserInfo(data) {
  return request({
    url: '/user/info/',
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid
    }
  })
}
export function getstatus(data) {
  return request({
    url: '/user/getstatus/',
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid
    }
  })
}
export function admingetUserInfo(data) {
  return request({
    url: '/user/info/',
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid
    }
  })
}
export function transportstream(data) {
  return request({
    url: '/user/transportstream/',
    method: 'post',
    data
  })
}
export function getillegaldata(data) {
  return request({
    url: '/user/getillegaldata/',
    method: 'get',
    params: {
      viewUserUuid: data.userid,
      start_time:data.start_time,
      end_time:data.end_time,
      split:data.split,
      unit:data.unit
    }
  })
}
export function logout(data) {
  return request({
    url: '/user/logout/',
    method: 'post',
    params: {
      token: data.token,
      roles: data.roles
    }
  })
}

export function userinfoupdate(data) {
  return request({
    url: '/user/info/', //与后端urls有关
    method: 'post',
    data
  })
}
export function admingetuser() {
  return request({
    url: '/adminuser/admingetuser/', //与后端urls有关
    method: 'get',
  })
}
export function admindeleteuser(data) {
  return request({
    url: '/adminuser/admindeleteuser/', //与后端urls有关
    method: 'get',
    params: {
      userid: data.userid
    }
  })
}
export function getusermobile(data) {
  return request({
    url: '/user/mobile/', //与后端urls有关
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid,
      search:data.search
    }
  })
}
export function getuserdrink(data) {
  return request({
    url: '/user/drink/', //与后端urls有关
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid,
      search:data.search
    }
  })
}

export function getusertired(data) {
  return request({
    url: '/user/tired/', //与后端urls有关
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid,
      search:data.search
    }
  })
}


export function getusersmoke(data) {
  return request({
    url: '/user/smoke/', //与后端urls有关
    method: 'get',
    params: {
      viewUserUuid: data.viewUserUuid,
      search:data.search
    }
  })
}
export function deletedrink(data) {
  return request({
    url: '/user/deletedrink/', //与后端urls有关
    method: 'get',
    params: {
      id: data.id
    }
  })
}
export function deletemobile(data) {
  return request({
    url: '/user/deletemobile/', //与后端urls有关
    method: 'get',
    params: {
      id: data.id,
    }
  })
}
export function deletesmoke(data) {
  return request({
    url: '/user/deletesmoke/', //与后端urls有关
    method: 'get',
    params: {
      id: data.id
    }
  })
}
export function deletetired(data) {
  return request({
    url: '/user/deletetired/', //与后端urls有关
    method: 'get',
    params: {
      id: data.id
    }
  })
}
