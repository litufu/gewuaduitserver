const { hash, compare } = require('bcrypt')
const crypto = require('crypto')
const { sign } = require('jsonwebtoken')
const { APP_SECRET, getUserId } = require('../utils')
const emailGenerator = require('../emailGenerator');

const Mutation = {
  signup: async (parent, { name, email, password }, ctx) => {
    const hashedPassword = await hash(password, 10)

    const resetPasswordToken = crypto.randomBytes(64).toString('hex')
    const validateEmailToken = crypto.randomBytes(64).toString('hex')

    const user = await ctx.prisma.createUser({
      name,
      email,
      password: hashedPassword,
      resetPasswordToken,
      validateEmailToken,
    })
    
    emailGenerator.sendWelcomeEmail(user, ctx)

    return {
      token: sign({ userId: user.id }, APP_SECRET),
      user,
    }
  },
  sendLinkValidateEmail:async (parent, args, ctx) => {
    // 发送验证链接到邮箱
    const userId = getUserId(ctx)
    let userMe = await ctx.prisma.user({ id: userId })

    return emailGenerator.sendWelcomeEmail(userMe, ctx)
    .then(data => {
      return userMe
    })
    .catch(data => {
      throw new Error(`错误 ${data}. 无法发送验证链接到邮箱: ${userMe.email}`)
    })
  },
  resetPassword:async (parent, {password,resetPasswordToken}, ctx) => {
    // 发送重置密码链接到邮箱，重新设置密码
    const userCheck = await ctx.prisma.user({ resetPasswordToken })
    if (!userCheck) {
      throw new Error(`重置密码链接无效`)
    } else {
      if (userCheck.resetPasswordExpires < new Date().getTime()) {
        throw new Error(`重置密码链接已过期`)
      }
      const hashpassword = await hash(password, 10)
      const user = await ctx.prisma.updateUser({
        where: { resetPasswordToken: resetPasswordToken },
        data: {
          password: hashpassword,
          resetPasswordExpires: new Date().getTime()
        }
      })
      return {
        token: sign({ userId: user.id }, APP_SECRET),
        user
      }
    }
  },
  validateEmail:async (parent, {validateEmailToken}, ctx) => {
    // 验证邮箱链接
    const userCheck = await ctx.prisma.user({ validateEmailToken })
    if (!userCheck) {
      throw new Error(`没有发现该用户.`)
    } else {
      if (userCheck.emailvalidated) {
        throw new Error(`用户已经验证`)
      }
    }
  
    const user = await ctx.prisma.updateUser({
      // Must check resetPasswordExpires
      where: { validateEmailToken },
      data: {
        emailvalidated: true
      }
    })
    return {
      token: sign({ userId: user.id }, APP_SECRET),
      user
    }
  },
  login: async (parent, { email, password }, ctx) => {
    const user = await ctx.prisma.user({ email })
    if (!user) {
      throw new Error(`邮箱错误: ${email}`)
    }
    const passwordValid = await compare(password, user.password)
    if (!passwordValid) {
      throw new Error('密码错误')
    }
    return {
      token: sign({ userId: user.id }, APP_SECRET),
      user,
    }
  },
  forgetPassword:async (parent, { email }, ctx) => {
    // 忘记密码，发送重置密码链接到邮箱
    const user = await ctx.prisma.user({ email })
    if (!user) {
      throw new Error(`邮箱错误: ${email}`)
    }
    try {
      let uniqueId = crypto.randomBytes(64).toString('hex')
      await ctx.prisma.updateUser({
        where: { id: user.id },
        data: {
          resetPasswordExpires: new Date().getTime() + 1000 * 60 * 60 * 5, // 5 hours
          resetPasswordToken: uniqueId
        }
      })
      emailGenerator.sendForgetPassword(uniqueId, email, ctx)
    } catch (e) {
      return e
    }
    return user
  },
  updatePassword:async (parent, { oldPassword,newPassword }, ctx) => {
    // 更新密码
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    const oldPasswordValid = await bcrypt.compare(oldPassword, user.password)
    if (!oldPasswordValid) {
      throw new Error('老密码错误，请重试.')
    }
    const newPasswordHash = await bcrypt.hash(newPassword, 10)
    
    const newUser = await ctx.prisma.updateUser({
        where: { id: userId },
        data: { password: newPasswordHash }
      })
    
    return newUser
  },
  contactToAccountingFirm:async (parent, { accountingFirmCode }, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    
    const newUser = await ctx.prisma.updateUser({
        where: { id: userId },
        data: { accountingFirm: {connect:{code:accountingFirmCode}} }
      })
    
    return newUser
  },
  createCustomer:async (parent, { name,code,type,nature }, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    // 检查用户是否已经关联了会计师事务所
    const accountingFirm = await ctx.prisma.user({ id: userId }).accountingFirm()
    if (!accountingFirm){
      throw new Error("尚未关联会计师事务所，请在个人设置中关联会计师事务所")
    }
    // 检查会计师事务所是否已经有了该客户
    const company = await ctx.prisma.company({name})
    if (company){
      throw new Error("客户已经存在，无需重复创建")
    }
    
    const newcompany = await ctx.prisma.createCompany({
      name,
      code,
      type,
      nature
    })
    
    return newcompany
  },
}

module.exports = {
  Mutation,
}