import Vue from "vue"; // 引入 Vue 是因为要用到 Vue.extend() 这个方法
import message from "./Message.vue"; // 引入刚才的 toast 组件


const Toast = function () {
  instance = new ToastConstructor().$mount(); // 渲染组件
};

let messageConstructor = Vue.extend(message); // 这个在前面的前置知识内容里面有讲到
let instance;

const Message = function (options = {}) {
  instance = new messageConstructor({
    data: options // 这里的 data 会传到 message.vue 组件中的 data 中，当然也可以写在 props 里
  }); // 渲染组件
  document.body.appendChild(instance.$mount().$el); // 挂载到 body 下
};

// 在这里将调用的方法分为两类
["success", "error"].forEach(type => {
  Message[type] = options => {
    options.type = type;
    return Message(options);
  };
})
export default Message;
