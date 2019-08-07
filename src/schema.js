const { gql } = require('apollo-server');

const typeDefs = gql`
  type Query {
    me: User
  }

  type Mutation {
    signup(email: String!, password: String!, name: String): AuthPayload!
    login(email: String!, password: String!): AuthPayload!
    
  }

 
  type AuthPayload {
    token: String!
    user: User!
  }

 
  type User {
    id: ID!
    email: String!
    name: String
   }
 
`;
module.exports = typeDefs;