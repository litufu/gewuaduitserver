const MergeProject = {
  sonCompanies: ({ id }, args, context) => {
        return context.prisma.mergeProject({ id }).sonCompanies()
    },
    parentCompany: ({ id }, args, context) => {
      return context.prisma.mergeProject({ id }).parentCompany()
    },
    users: ({ id }, args, context) => {
        return context.prisma.mergeProject({ id }).users()
    },
  }
    
  module.exports = {
    MergeProject,
  }