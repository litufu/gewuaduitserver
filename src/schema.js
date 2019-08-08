const { gql } = require('apollo-server');

const typeDefs = gql`
  scalar DateTime

  type Query {
    me: User
  }

  type Mutation {
    signup( email: String!, password: String!, name: String!): AuthPayload!
    sendLinkValidateEmail: User! #发送验证链接到邮箱
    resetPassword(password: String!, resetPasswordToken: String!): AuthPayload!
    validateEmail(validateEmailToken: String!): AuthPayload!
    login(email: String!, password: String!): AuthPayload!
    forgetPassword(email: String!): User!
    updatePassword(oldPassword: String, newPassword: String!): User!
  }

 
  type AuthPayload {
    token: String!
    user: User!
  }

  enum Role {
      ADMIN
      CUSTOMER
  }

  type User {
    id: ID!
    email: String!
    emailvalidated: Boolean!
    validateEmailToken: String!
    createdAt: DateTime!
    updatedAt: DateTime!
    resetPasswordToken: String! 
    resetPasswordExpires: Float
    name: String!
    role: Role!
  }
 
 
`;
module.exports = typeDefs;