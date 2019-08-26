"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var prisma_lib_1 = require("prisma-client-lib");
var typeDefs = require("./prisma-schema").typeDefs;

var models = [
  {
    name: "Role",
    embedded: false
  },
  {
    name: "User",
    embedded: false
  },
  {
    name: "AccountingFirm",
    embedded: false
  },
  {
    name: "CompanyType",
    embedded: false
  },
  {
    name: "CompanyNature",
    embedded: false
  },
  {
    name: "Company",
    embedded: false
  },
  {
    name: "Holder",
    embedded: false
  },
  {
    name: "Project",
    embedded: false
  },
  {
    name: "ProjectRole",
    embedded: false
  },
  {
    name: "Member",
    embedded: false
  },
  {
    name: "DataRecord",
    embedded: false
  },
  {
    name: "FileType",
    embedded: false
  },
  {
    name: "File",
    embedded: false
  },
  {
    name: "SubjectContrast",
    embedded: false
  },
  {
    name: "TbSubject",
    embedded: false
  },
  {
    name: "FSSubject",
    embedded: false
  }
];
exports.Prisma = prisma_lib_1.makePrismaClientClass({
  typeDefs,
  models,
  endpoint: `http://192.168.99.100:4466`
});
exports.prisma = new exports.Prisma();
