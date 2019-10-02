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
  getTB:async(parent,{projectId,type},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const types = ["unAudited","adjustment","audited"]
    if(types.indexOf(type)===-1){
      throw new Error("tb类型错误")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    const getTBPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_tb.py') 
    const getTBProcess = spawnSync('python',[getTBPath, dbPath,startTimeStr,endTimeStr,type]);
    const tb = getTBProcess.stdout.toString() 
    return tb
  },
  getPreviousTb: async(parent,{projectId,statement},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    
    const type = "audited"
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTime = new Date(project.startTime)
    const endTime = new Date(project.endTime)
    const previousStartTime = new Date(startTime.getFullYear()-1,startTime.getMonth(),startTime.getDate())
    let previousEndTime
    if(statement==="资产负债表"){
      previousEndTime = new Date(endTime.getFullYear()-1,11,31)
    }else if(statement==="利润表"){
      previousEndTime = new Date(endTime.getFullYear()-1,endTime.getMonth(),endTime.getDate())
    }
    const startTimeStr = dateToString(previousStartTime)
    const endTimeStr = dateToString(previousEndTime)
    const getTBPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_tb.py') 
    const getTBProcess = spawnSync('python',[getTBPath, dbPath,startTimeStr,endTimeStr,type]);
    const tb = getTBProcess.stdout.toString() 
    return tb
  },
  getSubjects: async(parent,{projectId},ctx)=>{
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
    const getSubjectsPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_subjects.py') 
    const getSubjectsProcess = spawnSync('python',[getSubjectsPath, dbPath,startTimeStr,endTimeStr]);
    const subjects = getSubjectsProcess.stdout.toString() 
    return subjects
  },
  getAuxiliaryNames:async(parent,{projectId},ctx)=>{
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
    const getAuxiliaryNamesPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_auxiliary_names.py') 
    const getAuxiliaryNamesProcess = spawnSync('python',[getAuxiliaryNamesPath, dbPath,startTimeStr,endTimeStr]);
    const names = getAuxiliaryNamesProcess.stdout.toString() 
    return names
  },
  getAuxiliaries:async(parent,{projectId},ctx)=>{
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
    const getAuxiliariesPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_auxiliaries.py') 
    const getAuxiliariesProcess = spawnSync('python',[getAuxiliariesPath, dbPath,startTimeStr,endTimeStr]);
    const auxiliaries = getAuxiliariesProcess.stdout.toString() 
    return auxiliaries
  },
  getAduitAdjustments:async(parent,{projectId},ctx)=>{
    const project = await ctx.prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await ctx.prisma.project({id:projectId}).accountingFirm()
    const company = await ctx.prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const endTimeStr = dateToString(new Date(project.endTime))
    const getAduitAdjustmentPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_aduit_adjustment.py') 
    const getAduitAdjustmentProcess = spawnSync('python',[getAduitAdjustmentPath, dbPath,endTimeStr]);
    const subjects = getAduitAdjustmentProcess.stdout.toString() 
    return subjects
  },
  stdSubjects:(parent,args,ctx)=>{
    return ctx.prisma.stdSubjects()
  },
  getProfitAndLossCarryOverStatus:async(parent,{projectId},ctx)=>{
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
    const checkProfitAndLossCarryOverPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/check_profit_and_loss_carry_over.py') 
    const checkProfitAndLossCarryOverProcess = spawnSync('python',[checkProfitAndLossCarryOverPath, dbPath,startTimeStr,endTimeStr]);
    const res = checkProfitAndLossCarryOverProcess.stdout.toString() 
    return res
  },
  getChangeReasons:async(parent,{projectId,statement,audit},ctx)=>{
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
    const getChangeReasonPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/get_change_reason.py') 
    const getChangeReasonProcess = spawnSync('python',[getChangeReasonPath, dbPath,startTimeStr,endTimeStr,statement,audit]);
    const res = getChangeReasonProcess.stdout.toString() 
    return res
  },
}

module.exports = {
  Query,
}