const { getUserId ,dateToString} = require('../utils')
const _ = require('lodash');
const {  spawnSync} = require('child_process');
const path = require('path')

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
      return []
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
  checkImportData:async(parent,{projectId},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    // 检查数据路数的正确性
    const checkImportDataPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/check_import_data.py') 
    const checkImportDataProcess = spawnSync('python',[checkImportDataPath, dbPath,startTimeStr,endTimeStr]); 
    if(_.trim(checkImportDataProcess.stdout.toString())==="true"){
      return true
    }
    return false
  },
  getSubjectBalance:async(parent,{projectId},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    // 检查数据路数的正确性
    const getSubjectBalancePath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_subject_balance.py') 
    const getSubjectBalanceProcess = spawnSync('python',[getSubjectBalancePath, dbPath,startTimeStr,endTimeStr]); 
    return getSubjectBalanceProcess.stdout.toString()
  },
  getChronologicalAccount:async(parent,{projectId,subjectNum,grade},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    const getChronologicalAccountPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_chronological_account.py') 
    const getChronologicalAccountProcess = spawnSync('python',[getChronologicalAccountPath, dbPath,startTimeStr,endTimeStr,subjectNum,grade]); 
    return getChronologicalAccountProcess.stdout.toString()
  },
  getTB:async(parent,{projectId},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    const getTBPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_tb.py') 
    const getTBProcess = spawnSync('python',[getTBPath, dbPath,startTimeStr,endTimeStr]);
    const tb = getTBProcess.stdout.toString() 
    return tb
  },
}

module.exports = {
  Query,
}