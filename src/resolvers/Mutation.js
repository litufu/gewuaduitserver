const { hash, compare } = require('bcrypt')
const fs = require("fs")
const crypto = require('crypto')
const mkdirp = require('mkdirp') 
const path = require('path')
const { spawn, spawnSync} = require('child_process');
const { sign } = require('jsonwebtoken')
const { APP_SECRET, getUserId,storeFS,UPLOAD_DIR,ALLOW_UPLOAD_TYPES,dateToString,delDir } = require('../utils')
const emailGenerator = require('../emailGenerator');

mkdirp.sync(UPLOAD_DIR)

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
    const oldPasswordValid = await compare(oldPassword, user.password)
    if (!oldPasswordValid) {
      throw new Error('老密码错误，请重试.')
    }
    const newPasswordHash = await hash(newPassword, 10)
    
    const newUser = await ctx.prisma.updateUser({
        where: { id: userId },
        data: { password: newPasswordHash }
      })
    
    return newUser
  },
  contactToAccountingFirm:async (parent, { accountingFirmName }, ctx) => {
    const userId = getUserId(ctx)
    const user = await ctx.prisma.user({ id: userId })
    if (!user) {
      throw new Error("用户不存在")
    }
    
    const newUser = await ctx.prisma.updateUser({
        where: { id: userId },
        data: { accountingFirm: {connect:{name:accountingFirmName}} }
      })
    
    return newUser
  },
  createCustomer:async (parent, { name,type,nature }, ctx) => {
    
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
      type,
      nature,
      accountingFirms:{connect:{id:accountingFirm.id}}
    })
    // 建立公司数据库
    const db_name = `${accountingFirm.id}-${newcompany.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    const databasePath = path.join(path.resolve(__dirname, '..'), './pythonFolder/database.py')
    // 1/创建数据库
    const initDataBaseProcess = spawn('python',[databasePath, dbPath]);
    initDataBaseProcess.stdout.on('data', (data) => {
      if(data==="success"){
        console.log("数据库建立成功")
      }
    });
    initDataBaseProcess.stderr.on('data', (data) => {
      throw new Error(`数据库建立失败${data}`)
    });
    // 2/初始化数据库
    const initDataPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/init_data.py')
    const initDataStructureProcess  = spawn('python',[initDataPath, dbPath]);
    initDataStructureProcess.stdout.on('data', (data) => {
      if(data==="success"){
        console.log("数据库初始化成功,下一步可以导入数据")
      }
    });
    initDataStructureProcess.stderr.on('data', (data) => {
      throw new Error(`初始数据失败${data}`)
    });

    // 搜索公司基本信息
    const filepath = path.join(path.resolve(__dirname, '..'), './pythonFolder/download_companyinfo.py')
    const pythonProcess = spawn('python',[filepath, name]);
    pythonProcess.stdout.on('data', async (data) => {
        res = JSON.parse(data)
        if(Array.isArray(res)){
          for (let i=0;i<res.length;i++) {
            const ratio = parseFloat(res[i].ratio.replace('%'))
            const holderName = res[i].holder_name
            await ctx.prisma.createHolder({
              name:holderName,
              ratio,
              company:{connect:{name}}
            })
          }
        }else{
          await ctx.prisma.updateCompany({
            where: { name },
            data: {
              code:res.code,
              address:res.address,
              legalRepresentative:res.legalRepresentative,
              establishDate:res.establishDate,
              registeredCapital:res.registeredCapital,
              paidinCapital:res.paidinCapital,
              businessScope:res.businessScope
            }
          })
        }
    });
    
    pythonProcess.stderr.on('data', (data) => {
       throw new Error(`客户信息下载失败，请确认客户名称是否正确${data}`)
    });

    pythonProcess.on('exit', (code) => {
      if(code!==0){
        throw new Error(`客户信息下载失败，请确认客户名称是否正确`)
      }
    });
    
    return newcompany
  },
  uploadDataFiles:async (parent, { uploads,companyName,startTime,endTime}, ctx) => {
    // 验证上传者
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

    const startTimeStr = dateToString(new Date(startTime))
    const endTimeStr = dateToString(new Date(endTime))
    
    // 检查上传文件的类型
    for(const upload of uploads){
      // 解析上传文件
      const {  mimetype } = await upload.file
      if(ALLOW_UPLOAD_TYPES.indexOf(mimetype)=== -1){
        throw new Error("上传数据类型不正确")
      }
    }

    // 验证公司
    const company = await ctx.prisma.company({ name: companyName })
    if(!company){
      throw new Error("公司名称不正确")
    }

    const db_name = `${accountingFirm.id}-${company.id}.sqlite`
    const dbPath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
    console.log(db_name)
    console.log(dbPath)
    const files = []
    for(const upload of uploads){
      // 解析上传文件
      const { createReadStream, filename, mimetype } = await upload.file
      const stream = createReadStream()
      // 存储文件记录
      const file = await ctx.prisma.createFile({
        path:UPLOAD_DIR,
        filename,
        mimetype,
        type:upload.type
      })
      // 存储文件
      const storeFilePath = `${UPLOAD_DIR}/${file.id}-${filename}`
      await storeFS({ storeFilePath,stream })
     
    //  读取文件并存储到数据库
      const importDataPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/import_data.py') 
      const uploadType = upload.type
      const importDataProcess = spawn('python',[importDataPath, dbPath,startTimeStr,endTimeStr,storeFilePath,uploadType]); 
      importDataProcess.stdout.on('data', async (data) => {
          console.log(data)
      })
      importDataProcess.stderr.on('data', (data) => {
        throw new Error(`数据录入失败${data}`)
      });
      importDataProcess.on('close', (code) => {
        console.log(`数据录入完成 ${code}`);
        fs.unlink(storeFilePath, function(err) {
          if (err) {
              return console.error(err);
          }
          console.log("文件删除成功！");
        })
      });
      const dataRecords = await ctx.prisma.dataRecords({
        where:{
          AND:[
            {accountingFirm:{id:accountingFirm.id}},
            {company:{name:companyName}},
            {startTime},
            {endTime},
          ]
        }
      })
      if(dataRecords.length>0){
        const dataRecord = dataRecords[0]
        await ctx.prisma.updateDataRecord({
          where:{id:dataRecord.id},
          data:{
            files:{connect:{id:file.id}},
            users:{connect:{id:userId}}
          }
        })
      }else{
        await ctx.prisma.createDataRecord({
          startTime,
          endTime,
          accountingFirm:{connect:{id:accountingFirm.id}},
          company:{connect:{name:companyName}},
          files:{connect:{id:file.id}},
          users:{connect:{id:userId}}
        })
      }
      // 登记文件信息
      
      files.push(file)
    }
    // // 检查数据路数的正确性
    // const checkImportDataPath = path.join(path.resolve(__dirname, '..'), './pythonFolder/check_import_data.py') 
    // const checkImportDataProcess = spawn('python',[checkImportDataPath, dbPath,startTimeStr,endTimeStr]); 
    // checkImportDataProcess.stdout.on('data', async (data) => {
    //   console.log(data)
    // })
    // checkImportDataProcess.stderr.on('data', (data) => {
    //   throw new Error(`数据检查逻辑失败${data}`)
    // });
    // checkImportDataProcess.on('close', (code) => {
    //   console.log(`数据逻辑检查完成 ${code}`);
    // });
    
    return files
  },
  addDataRecordUsers:async (parent, { userEmails,companyName,startTime,endTime}, ctx) => {
    // 验证上传者
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
        ]
      }
    })
    const emails = userEmails.map(email=>({email}))
    if(dataRecords.length>0){
      const newDataRecord = await ctx.prisma.updateDataRecord({
        where: {id:dataRecords[0].id},
          data: {
            users:{connect:emails}
          }
      })
      return newDataRecord
    }else{
      throw new Error("未发现数据记录")
    }
  },
  createProject:async (parent, { members,companyName,startTime,endTime}, ctx) => {
    // 验证上传者
    console.log(members)
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
        ]
      }
    })
    // 将所有的用户添加到数据授权列表
    const emails = members.map(member=>({email:member.email}))
    if(dataRecords.length>0){
      await ctx.prisma.updateDataRecord({
        where: {id:dataRecords[0].id},
          data: {
            users:{connect:emails}
          }
      })
      const createMembers = members.map(member=>({
        role:member.role,
        user:{connect:{email:member.email}}
        
      }))
      const project = await ctx.prisma.createProject({
        startTime,
        endTime,
        accountingFirm:{connect:{id:accountingFirm.id}},
        company:{connect:{name:companyName}},
        members:{
          create:createMembers
        }
      })
      return project
    }else{
      throw new Error("未发现数据记录")
    }
  },
}

module.exports = {
  Mutation,
}