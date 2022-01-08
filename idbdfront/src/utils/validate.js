/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['Soceremite','admin','test','police']
  return valid_map.indexOf(str.trim()) >= 0
}

/**
 * @param {string} str
 * @returns {Boolean}
 * */
// 这是新增的验证邮箱的函数
export function validEmail(str) {
  const emailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
  return emailReg.test(str)
}
