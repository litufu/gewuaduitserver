const { verify } = require('jsonwebtoken')
const fs = require('fs')
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
const DB_DIR = './db'
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
  delDir
}