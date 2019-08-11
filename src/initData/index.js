const Papa = require('papaparse');
const fs = require('fs')
const {prisma} = require('../generated/prisma-client')

const accountingfirmFile = './src/initData/data/accountingfirm.csv'

const readFile = function (fileName, encode) {
  return new Promise(function (resolve, reject) {
    fs.readFile(fileName, encode, function (error, data) {
      if (error) return reject(error);
      resolve(data);
    });
  });
};

const parseCsv = function (data) {
  return new Promise(function (resolve, reject) {
    Papa.parse(data, {
      complete: function (results) {
        resolve(results);
      }
    });
  });
};

// 添加会计师事务所信息

async function addAccountingFirm() {
  try {
    const file = await readFile(accountingfirmFile, 'utf8')
    const results = await parseCsv(file)
    for (const value of results.data) {
      try {
        const accountingFirm = await prisma
          .createAccountingFirm({
            code: value[2],
            name: value[3],
            address: value[4],
            contact: value[5],
            phone: value[6],
            email:"",
          })
        console.log(accountingFirm);
      } catch (err) {
        console.log(err)
        continue
      }
    }
  } catch (err) {
    console.log(err);
  }
}

addAccountingFirm()