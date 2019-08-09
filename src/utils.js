const { verify } = require('jsonwebtoken')

// 企业邮箱
const userMail = "aduit@gewu.org.cn"
const passMail = "litufu001!2"
const service = "qiye.aliyun"

const APP_SECRET = 'appsecret321'

class AuthError extends Error {
  constructor() {
    super('Not authorized')
  }
}

function getUserId(context) {
  const Authorization = context.request.get('Authorization')
  if (Authorization) {
    const token = Authorization.replace('Bearer ', '')
    const verifiedToken = verify(token, APP_SECRET)
    return verifiedToken && verifiedToken.userId
  }
}

module.exports = {
  getUserId,
  APP_SECRET,
  userMail,
  passMail,
  service,
}