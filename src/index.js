const { ApolloServer } = require('apollo-server');

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
  });

// if (process.env.NODE_ENV !== 'test')
server
.listen({ port: 4000 })
.then(({ url }) => console.log(`🚀 app running at ${url}`));
    
