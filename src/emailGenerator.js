const nodemailer = require('nodemailer')
const { userMail, passMail } = require('./utils')

module.exports = {
  async sendWelcomeEmail (user, ctx) {
    var mailer = nodemailer.createTransport({
      service: 'qiye.aliyun',
      auth: {
        user: userMail,
        pass: passMail
      }
    })

    var mailOptions = {
      to: user.email,
      from: 'aduit@gewu.org.cn',
      subject: '欢迎来到格物在线审计',
      html: `
      <div>你好 ${user.name}</div>
      <div>很高兴你能来到格物在线审计.</div>
        <div>请验证你的邮箱.
           ${ctx.request.headers.origin}/validateEmail?validateEmailToken=${user.validateEmailToken}
        </div>
    `
    }
    return mailer.sendMail(mailOptions)
  },
  sendForgetPassword (uniqueId, email, ctx) {
    var mailer = nodemailer.createTransport({
      service: 'qiye.aliyun',
      auth: {
        user: userMail,
        pass: passMail
      }
    })

    var mailOptions = {
      to: email,
      from: 'aduit@gewu.org.cn',
      subject: '忘记密码 - 格物在线审计',
      html: `
      <div>你好</div>
      <div>请点击链接重新设置密码.
         ${ctx.request.headers.origin}/resetPassword?resetPasswordToken=${uniqueId}
      </div>
    `
    }
    mailer.sendMail(mailOptions, function (err) {
      if (err) {
        console.log(err)
      } else {
        console.log('Mail sent to: ' + email)
      }
    })
  }
}
