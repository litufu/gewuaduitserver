const Company = {
    holders: ({ id }, args, context) => {
        return context.prisma.company({ id }).holders()
    },
  
  }
    
  module.exports = {
    Company,
  }