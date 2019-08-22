const Project = {
    accountingFirm: ({ id }, args, context) => {
        return context.prisma.project({ id }).accountingFirm()
    },
    company: ({ id }, args, context) => {
        return context.prisma.project({ id }).company()
    },
    members: ({ id }, args, context) => {
        return context.prisma.project({ id }).members()
    },
  
  }
    
  module.exports = {
    Project,
  }