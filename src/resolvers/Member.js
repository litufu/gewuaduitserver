const Member = {
    project: ({ id }, args, context) => {
        return context.prisma.member({ id }).project()
    },
    user: ({ id }, args, context) => {
        return context.prisma.member({ id }).user()
    },
  
  }
    
  module.exports = {
      Member,
  }