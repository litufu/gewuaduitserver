const path = require('path')

const db_name = "sdfe-123.sqlite"
const databasePath = path.join(path.resolve(__dirname, '../../db'), `./${db_name}`)
const pythonProcess = spawn('python',[databasePath]);
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