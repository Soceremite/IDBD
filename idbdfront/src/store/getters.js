const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  title: state => state.app.title,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  user: state => state.user.user,
  userinfo: state => state.user.userinfo,
  //添加权限
  roles: state => state.user.roles,
  permission_routes: state => state.permission.routes
}
export default getters
