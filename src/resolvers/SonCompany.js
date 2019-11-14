const SonCompany = {
    company: ({ id }, args, context) => {
        return context.prisma.sonCompany({ id }).company()
    },
  }
    
  module.exports = {
    SonCompany,
  }