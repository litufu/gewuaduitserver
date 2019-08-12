const { getUserId } = require('../utils')

const Query = {
  me: (parent, args, ctx) => {
    const userId = getUserId(ctx)
    return ctx.prisma.user({ id: userId })
  },
  emailHasTaken:async (parent, {email}, ctx) => {
    const user = await ctx.prisma.user({ email })
    if (!user) {
      return false
    }else{
      return true
    }
  },
  accountingFirms:async (parent, {inputvalue}, ctx) => {
    const firms = await ctx.prisma.accountingFirms({ 
      where: { name_starts_with: inputvalue },
      first: 10
    })
   return firms
  },
}

module.exports = {
  Query,
}