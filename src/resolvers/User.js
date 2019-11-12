const User = {
  accountingFirm: ({ id }, args, context) => {
      return context.prisma.user({ id }).accountingFirm()
  },
  projects: ({ id }, args, context) => {
      return context.prisma.user({ id }).projects()
  },
  mergeProjects: ({ id }, args, context) => {
    return context.prisma.user({ id }).mergeProjects()
  },
  dataRecords: ({ id }, args, context) => {
    return context.prisma.user({ id }).dataRecords()
  },

}
  
module.exports = {
    User,
}