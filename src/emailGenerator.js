const nodemailer = require('nodemailer')
const { userMail, passMail } = require('./utils')

module.exports = {
  async sendWelcomeEmail (user, ctx) {
    const mailer = nodemailer.createTransport({
      service: 'qiye.aliyun',
      auth: {
        user: userMail,
        pass: passMail
      }
    })

    const mailOptions = {
      to: user.email,
      from: 'aduit@gewu.org.cn',
      subject: '欢迎来到格物在线审计',
      html: `
      <div>你好 ${user.name}</div>
      <div>请点击下面链接进行验证</div>
        <div>
           ${ctx.req.headers.origin}/validateEmail?validateEmailToken=${user.validateEmailToken}
        </div>
    `
    }
    return mailer.sendMail(mailOptions)
  },
  sendForgetPassword (uniqueId, email, ctx) {
    const mailer = nodemailer.createTransport({
      service: 'qiye.aliyun',
      auth: {
        user: userMail,
        pass: passMail
      }
    })

    const mailOptions = {
      to: email,
      from: 'aduit@gewu.org.cn',
      subject: '忘记密码 - 格物在线审计',
      html: `
      <div>你好,请点击下面链接重新设置密码.</div>
      <div>
         ${ctx.req.headers.origin}/resetPassword?resetPasswordToken=${uniqueId}
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
