const { Query } = require('./Query')
const { Mutation } = require('./Mutation')
const { User } = require('./User')
const { Company } = require('./Company')
const { Holder } = require('./Holder')
// const {GraphQLUpload} = require("apollo-server-express")

const resolvers = {
  Query,
  Mutation,
  User,
  Company,
  Holder,
}

module.exports = {
  resolvers,
}