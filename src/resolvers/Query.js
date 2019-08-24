const { getUserId } = require('../utils')

const Query = {
  me: (parent, args, ctx) => {
    const userId = getUserId(ctx)
    return ctx.prisma.user({ id: userId })
  },
  colleagues:async (parent, {name}, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    // 验证会计师事务所
    const accountingFirm = await ctx.prisma.user({ id: userId }).accountingFirm()
    if(!accountingFirm){
      throw new Error("你还没有加入会计师事务所，无法上传数据")
    }
    return ctx.prisma.users({
      where:{AND:[
        {accountingFirm:{id:accountingFirm.id}},
        {name_contains:name},
      ]}
    })
  },
  dataRecord:async (parent, {companyName,startTime,endTime}, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    // 验证会计师事务所
    const accountingFirm = await ctx.prisma.user({ id: userId }).accountingFirm()
    if(!accountingFirm){
      throw new Error("你还没有加入会计师事务所，无法上传数据")
    }
    const dataRecords = await ctx.prisma.dataRecords({
      where:{
        AND:[
          {accountingFirm:{id:accountingFirm.id}},
          {company:{name:companyName}},
          {startTime},
          {endTime},
          {users_some:{id:userId}}
        ]
      }
    })
    if(dataRecords.length>0){
      return dataRecords[0]
    }else{
      throw new Error("请确认已上传该公司该期间数据，并且你已被授权访问。")
    }
  },
  emailHasTaken:async (parent, {email}, ctx) => {
    const user = await ctx.prisma.user({ email })
    if (!user) {
      return false
    }else{
      return true
    }
  },
  accountingFirms:async (parent, {inputvalue}, ctx) => {
    const firms = await ctx.prisma.accountingFirms({ 
      where: { name_starts_with: inputvalue },
      first: 10
    })
   return firms
  },
  companies:async (parent, {inputvalue}, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    // 验证会计师事务所
    const accountingFirm = await ctx.prisma.user({ id: userId }).accountingFirm()
    if(!accountingFirm){
      throw new Error("你还没有加入会计师事务所，无法上传数据")
    }
    return ctx.prisma.user({ id: userId }).accountingFirm().customers({ 
      where: { name_contains: inputvalue },
      first: 10
    })
  },
  projects:async (parent, args, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    // 验证会计师事务所
    const accountingFirm = await ctx.prisma.user({ id: userId }).accountingFirm()
    if(!accountingFirm){
      throw new Error("你还没有加入会计师事务所，无法上传数据")
    }

    const projects = await ctx.prisma.projects({
      where:{
        AND:[
          {accountingFirm:{id:accountingFirm.id}},
          {members_some:{user:{id:userId}}}
        ]
      }
    })

    return projects
  },
}

module.exports = {
  Query,
}