const { gql } = require('apollo-server');

const typeDefs = gql`
  scalar DateTime

  type Query {
    me: User
    emailHasTaken(email:String!):Boolean!
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
    accountingFirm:AccountingFirm
    projects:[Project]
    dataRecords:[DataRecord]
  }

  type AccountingFirm{
    id: ID!
    name:String!
    code:String!
    address:String!
    phone:String!
    email:String!
    contact:String!
    employees:[User]
  }

  enum CompanyType {
    DOMESTIC
    OUTLANDS
  }

  enum CompanyNature{
    STATEOWNED
    LISTED
    PLANNEDLISTED
    OTHER
  }


  type Company{
    id: ID!
    type:CompanyType!
    nature:CompanyNature!
    name:String!
    code:String
    address:String
    legalRepresentative:String
    establishDate:DateTime
    registeredCapital:String
    paidinCapital:String
    businessScope:String
    holders:[Holder]
  }

  type Holder{
    id: ID!
    name:String!
    ratio:Float!
    company:Company!
  }

  type Project{
    id: ID!
    accountingFirm:AccountingFirm!
    company:Company!
    startTime:DateTime!
    endTime:DateTime!
    members:[Member]
  }

  enum ProjectRole{
    MANAGER
    PARTNER
    ASSISTANT
    QC
    REVIEWPARTNER
    JUDGE
    CPA
  }

  type Member{
    id: ID!
    project:Project!
    user:User!
    role:ProjectRole!
  }

  type DataRecord{
    id: ID!
    accountingFirm:AccountingFirm!
    company:Company!
    startTime:DateTime!
    endTime:DateTime!
    uploadTime:DateTime!
    uploadContent:String
    users:[User]
  }
 
 
`;
module.exports = typeDefs;