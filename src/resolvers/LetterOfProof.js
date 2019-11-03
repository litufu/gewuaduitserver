const LetterOfProof = {
    project: ({ id }, args, context) => {
        return context.prisma.letterOfProof({ id }).project()
    },
  
  }
    
  module.exports = {
    LetterOfProof,
  }