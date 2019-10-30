const _ = require("lodash")
const { verify } = require('jsonwebtoken')
const fs = require('fs')
const path = require('path')
// 企业邮箱
const userMail = "aduit@gewu.org.cn"
const passMail = "litufu001!2"
const service = "qiye.aliyun"

const APP_SECRET = 'appsecret321'

const companyNature = {
  "STATEOWNED":"国有企业",
  "LISTED":"上市公司",
  "PLANNEDLISTED":"拟上市公司",
  "OTHER":"其他公司"
}

class AuthError extends Error {
  constructor() {
    super('Not authorized')
  }
}

function getUserId(context) {
  const Authorization = (context.req.headers && context.req.headers.authorization) || '';
  if (Authorization) {
    const token = Authorization.replace('Bearer ', '')
    const verifiedToken = verify(token, APP_SECRET)
    return verifiedToken && verifiedToken.userId
  }
}

const UPLOAD_DIR = './uploads'
const DB_DIR = '../db'
const ALLOW_UPLOAD_TYPES = [
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/vnd.ms-excel"
]

const dateToString=(date)=>{
  const year = date.getFullYear()
  const month = date.getMonth()	+ 1
  const day = date.getDate()
  return `${year}-${month}-${day}`
}

function delDir(path){
    let files = [];
    if(fs.existsSync(path)){
        files = fs.readdirSync(path);
        files.forEach((file, index) => {
            let curPath = path + "/" + file;
            if(fs.statSync(curPath).isDirectory()){
                delDir(curPath); //递归删除文件夹
            } else {
                fs.unlinkSync(curPath); //删除文件
            }
        });
        fs.rmdirSync(path);
    }
}

const storeFS = ({ storeFilePath,stream }) => {
  return new Promise((resolve, reject) =>
    stream
      .on('error', error => {
        console.log(error)
        if (stream.truncated)
          // Delete the truncated file.
          fs.unlinkSync(storeFilePath)
        reject(error)
      })
      .pipe(fs.createWriteStream(storeFilePath))
      .on('error', error => {
        console.log(error)
        reject(error)
      }
        )
      .on('finish', () => {
        resolve({ storeFilePath })
      })
  )
}

const  getProjectDBPathStartTimeEndtime = async (projectId,prisma)=>{
  const project = await prisma.project({id:projectId})
    if(!project){
      throw new Error("未发现该项目")
    }
    const accountingFirm = await prisma.project({id:projectId}).accountingFirm()
    const company = await prisma.project({id:projectId}).company()
    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const startTimeStr = dateToString(new Date(project.startTime))
    const endTimeStr = dateToString(new Date(project.endTime))
    return {dbPath,startTimeStr,endTimeStr,project,company}
}

const companyType = (name)=>{

  let type
  if((name.indexOf("公司")!==-1) ||(name.indexOf("合伙")!==-1)){
    type = "公司"
  }else{
    type = "非公司"
  }
  return type
}

const deleteExistRelatedParty=async (ctx,company,obj,grade,relationship)=>{
  const relatedParties = await ctx.prisma.relatedParties({
    where:{
      AND:[
        {grade},
        {relationship_contains:relationship},
        {name:obj.name},
        {company:{id:company.id}}
      ]
    }
  })
  if(relatedParties.length>0){
    await ctx.prisma.deleteRelatedParty({id:relatedParties[0].id})
  }
}

const saveMainMembersToRelatedParty = async (ctx,company,members,grade)=>{
  if(members.length>0){
    for(let i=0;i<members.length;i++){
      let member = members[i]
      await deleteExistRelatedParty(ctx,company,member,grade,"公司高管")
      await ctx.prisma.createRelatedParty({
        grade,
        relationship:"公司高管",
        name:member.name,
        type:"非公司",
        company:{connect:{id:company.id}}
      })
    }
  }
}

const saveHoldersToRelatedParty= async (ctx,company,contolHolder,otherHolders,grade)=>{

  // 添加控股股东
  await deleteExistRelatedParty(ctx,company,contolHolder,grade,"控股股东")
  await ctx.prisma.createRelatedParty({
    grade,
    relationship:`控股股东-${contolHolder.ratio}`,
    name:contolHolder.name,
    type:companyType(contolHolder.name),
    company:{connect:{id:company.id}}
  })
  
  // 添加持股股东到关联方
  for(let i=0;i<otherHolders.length;i++){
    await deleteExistRelatedParty(ctx,company,otherHolders[i],grade,"持股股东")
    await ctx.prisma.createRelatedParty({
      grade,
      relationship:`持股股东-${otherHolders[i].ratio}`,
      name:otherHolders[i].name,
      type:companyType(otherHolders[i].name),
      company:{connect:{id:company.id}}
    })
  }
}

const saveCompanyToRelatedParty= async (ctx,company)=>{
  // 添加控股股东
  await deleteExistRelatedParty(ctx,company,company,0,"自身")
  await ctx.prisma.createRelatedParty({
    grade:0,
    relationship:"自身",
    name:company.name,
    type:"公司",
    company:{connect:{id:company.id}}
  })
}

const addCompanyInfo=async (ctx,res,type,nature)=>{
    let companyInfo = res.companyInfo
    let holders = res.holders
    let members = res.members
    // 增加公司信息
    const company = await ctx.prisma.createCompany({
      name:companyInfo.name,
      type:type,
      nature:nature,
      code:companyInfo.code,
      address:companyInfo.address,
      legalRepresentative:companyInfo.legalRepresentative,
      establishDate:companyInfo.establishDate,
      registeredCapital:companyInfo.registeredCapital,
      paidinCapital:companyInfo.paidinCapital,
      businessScope:companyInfo.businessScope
  })
  // 增加股东信息
  for (let i=0;i<holders.length;i++) {
    const ratio = parseFloat(holders[i].ratio.replace('%',""))
    const holderName = holders[i].holder_name
    await ctx.prisma.createHolder({
      name:holderName,
      ratio,
      company:{connect:{id:company.id}}
    })
  }
  // 增加主要成员信息
  for (let i=0;i<members.length;i++) {
    const post = members[i].post
    const Membername = members[i].name
    await ctx.prisma.createMainMember({
      name:Membername,
      post,
      company:{connect:{id:company.id}}
    })
  }
}

module.exports = {
  getUserId,
  APP_SECRET,
  userMail,
  passMail,
  companyNature,
  service,
  UPLOAD_DIR,
  DB_DIR,
  storeFS,
  ALLOW_UPLOAD_TYPES,
  dateToString,
  delDir,
  getProjectDBPathStartTimeEndtime,
  companyType,
  saveMainMembersToRelatedParty,
  saveHoldersToRelatedParty,
  saveCompanyToRelatedParty,
  addCompanyInfo
}