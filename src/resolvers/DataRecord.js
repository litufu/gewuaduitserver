const DataRecord = {
    accountingFirm: ({ id }, args, context) => {
        return context.prisma.dataRecord({ id }).accountingFirm()
    },
    company: ({ id }, args, context) => {
        return context.prisma.dataRecord({ id }).company()
    },
    files: ({ id }, args, context) => {
        return context.prisma.dataRecord({ id }).files()
    },
    users: ({ id }, args, context) => {
        return context.prisma.dataRecord({ id }).users()
    },
  
  }
    
  module.exports = {
    DataRecord,
  }