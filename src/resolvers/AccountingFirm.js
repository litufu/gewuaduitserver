const AccountingFirm = {
    customers: ({ id }, args, context) => {
        return context.prisma.accountingFirm({ id }).customers()
    },
    employees: ({ id }, args, context) => {
        return context.prisma.accountingFirm({ id }).employees()
    },
  
  }
    
  module.exports = {
    AccountingFirm,
  }