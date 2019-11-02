const { gql } = require('apollo-server-express');

const typeDefs = gql`
  scalar DateTime

  type Query {
    me: User
    colleagues(name:String!):[User]
    dataRecord(companyName:String!,startTime:DateTime!,endTime:DateTime!):DataRecord
    emailHasTaken(email:String!):Boolean!
    accountingFirms(inputvalue:String!):[AccountingFirm]
    companies(inputvalue:String!):[Company]
    company(projectId:String!):Company
    project(projectId:String!):Project
    projects:[Project]
    checkImportData(projectId:String):Boolean!
    getSubjectBalance(projectId:String):String!
    getChronologicalAccount(projectId:String!,subjectNum:String!,grade:Int!):String!
    getTB(projectId:String,type:String!):String!
    getPreviousTb(projectId:String,statement:String!):String!
    getAuxiliaries(projectId:String!):String!
    getAduitAdjustments(projectId:String!):String!
    stdSubjects:[StdSubject]
    getNoComputeTbSubjects:[TbSubject]
    getChangeReasons(projectId:String!,statement:String!,audit:String!):String!
    getEntryClassify(projectId:String!,recompute:String!):String!
    getChronologicalAccountByEntryNums(projectId:String!,record:String!):String!
    getCheckEntry(projectId:String!,ratio:Float,num:Int,integerNum:Int,recompute:String!):String!
    getSupplierAnalysis(projectId:String!):String!
    getCustomerAnalysis(projectId:String!):String!
    getAgeSetting(projectId:String!):String!
    getAccountAge(projectId:String!):String!
    getFirstNCustomersOrSuppliers(projectId:String!,num:Int!,type:String!):String!
    getCompanies(companyNames:[String]!):[Company]
    getStdCompanyNames(projectId:String!):[CompanyStdName]
    getCompanyDeal(projectId:String!,type:String!,num:Int!):[CompanyDeal]
    getRate(currencyType:String!,date:String!):String!
  }

  type Mutation {
    signup( email: String!, password: String!, name: String!): AuthPayload!
    sendLinkValidateEmail: User! #发送验证链接到邮箱
    resetPassword(password: String!, resetPasswordToken: String!): AuthPayload!
    validateEmail(validateEmailToken: String!): AuthPayload!
    login(email: String!, password: String!): AuthPayload!
    forgetPassword(email: String!): User!
    updatePassword(oldPassword: String, newPassword: String!): User!
    contactToAccountingFirm(accountingFirmName:String!):User!
    createCustomer(name:String!,type:CompanyType!,nature:CompanyNature!):Company!
    updateCompanyDataSettings(companyName:String!):Boolean!
    uploadDataFiles(uploads:[UploadTypeInput!]!,companyName:String!,startTime:DateTime!,endTime:DateTime!):[File]
    addDataRecordUsers(userEmails:[String],companyName:String!,startTime:DateTime!,endTime:DateTime!):DataRecord!
    createProject(members:[MemberInput],companyName:String!,startTime:DateTime!,endTime:DateTime!):Project
    addAduitAdjustment(projectId:String!,record:String!):Boolean!
    deleteAdutiAdjustment(projectId:String!,vocherNum:Int!,vocherType:String!):Boolean!
    modifyAduitAdjustment(projectId:String!,record:String!,vocherNum:Int!):Boolean!
    addSubject(projectId:String!,record:String!):Boolean!
    addAuxiliary(projectId:String!,record:String!):Boolean!
    addChangeReason(projectId:String!,record:String!):Boolean!
    ageSetting(projectId:String!,years:Int!,months:Int!,oneYear:Boolean!):Boolean!
    currentAccountHedging(projectId:String!):Boolean!
    computeAccountAge(projectId:String!):Boolean!
    downloadCompanyInfo(companyName:String!):Company
    downloadCustomerAndSupplierInfo(projectId:String!,num:Int!):Boolean!
    downloadRelatedPatiesCompany(companyName:String!,speed:String!):Company!
    addStdCompanyName(originName:String!,stdName:String!,projectId:String!):CompanyStdName
    setStandardizedAccountName(projectId:String!):Boolean!
  }



  input UploadTypeInput{
    file:Upload!
    type:String!
  }

  enum FileType{
    SUBJECTBALANCE
    CHRONOLOGICALACCOUNT
    AUXILIARYACCOUNTING
  }

  type File {
    id: ID!
    path: String!
    filename: String!
    mimetype: String!
    type:FileType!
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
    customers:[Company]
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

  type CompanyDeal{
    company:Company
    amount:Float!
    name:String!
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
    relatedParties:[RelatedParty]
  }

  type Holder{
    id: ID!
    name:String!
    ratio:Float!
    company:Company!
  }

  type RelatedParty{
    id: ID!
    grade:Int!
    relationship:String!
    type:String!
    name:String!
    company:Company!
  }

  input MemberInput{
    email:String!
    role:String!
  }

  type CompanyStdName{
    id: ID!
    dbName:String!
    originName:String!
    stdName:String!
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
    files:[File!]!
    users:[User] #授权使用者
  }

  type StdSubject{
    id: ID!
    code:String!
    name:String!
  }

  type TbSubject{
    id: ID!
    show:String!
    subject:String!
    direction:String!
    order:Int!
  }
  
`;
module.exports = typeDefs;