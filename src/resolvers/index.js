const { Query } = require('./Query')
const { Mutation } = require('./Mutation')
const { User } = require('./User')
const { Company } = require('./Company')
const { Holder } = require('./Holder')
const { DataRecord } = require('./DataRecord')
const { Project } = require('./Project')
const { Member } = require('./Member')
const {RelatedParty} = require('./RelatedParty')
// const {GraphQLUpload} = require("apollo-server-express")

const resolvers = {
  Query,
  Mutation,
  User,
  Company,
  Holder,
  DataRecord,
  Project,
  Member,
  RelatedParty,
}

module.exports = {
  resolvers,
}