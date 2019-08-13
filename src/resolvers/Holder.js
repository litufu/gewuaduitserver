const Holder = {
    company: ({ id }, args, context) => {
        return context.prisma.holder({ id }).company()
    },
  
  }
    
  module.exports = {
    Holder,
  }