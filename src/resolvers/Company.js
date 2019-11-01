const Company = {
    holders: ({ id }, args, context) => {
        return context.prisma.company({ id }).holders()
    },
    relatedParties: ({ id }, args, context) => {
      return context.prisma.company({ id }).relatedParties()
    },
  }
    
  module.exports = {
    Company,
  }