const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');

const typeDefs = require('./schema');
const { resolvers } = require('./resolvers')
const { prisma } = require('./generated/prisma-client')


const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: request => {
        return {
          ...request,
          prisma,
        }
      },
    uploads: {
      // Limits here should be stricter than config for surrounding
      // infrastructure such as Nginx so errors can be handled elegantly by
      // graphql-upload:
      // https://github.com/jaydenseric/graphql-upload#type-uploadoptions
      maxFileSize: 10000000, // 10 MB
      maxFiles: 20
    }
  });

const app = express();
server.applyMiddleware({ app });

// if (process.env.NODE_ENV !== 'test')
app.listen({ port: 5000 }, () =>
  console.log(`🚀 Server ready at http://localhost:5000${server.graphqlPath}`)
);
    
