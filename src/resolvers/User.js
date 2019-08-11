const User = {
  accountingFirm: ({ id }, args, context) => {
      return context.prisma.user({ id }).accountingFirm()
  },

}
  
module.exports = {
    User,
}