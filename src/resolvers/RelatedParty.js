const RelatedParty = {
    company: ({ id }, args, context) => {
        return context.prisma.relatedParty({ id }).company()
    },
  }
    
  module.exports = {
    RelatedParty,
  }