const Papa = require('papaparse');
const fs = require('fs')
const {prisma} = require('../generated/prisma-client')

const accountingfirmFile = './src/initData/data/accountingfirm.csv'
const subjectContrastFile = './src/initData/data/subject_contrast.csv'
const tbSubjectFile = './src/initData/data/tb.csv'
const fs2019File = './src/initData/data/fs_2019.csv'
const fs2018File = './src/initData/data/fs_2018.csv'
const stdSubjectFile = './src/initData/data/first_class.csv'

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

// 添加TB对照表信息

async function addFs(fsfile,name) {
  try {
    const file = await readFile(fsfile, 'utf8')
    const results = await parseCsv(file)
    for (const value of results.data) {
      if(value[0]==="fs_show"){
        continue
      }
      try {
        const fs2019 = await prisma
          .createFSSubject({
            show: value[0],
            subject: value[1],
            direction: value[2],
            name,
          })
        console.log(fs2019);
      } catch (err) {
        console.log(err)
        continue
      }
    }
  } catch (err) {
    console.log(err);
  }
}

// 添加TB对照表信息

async function addTbSubject() {
  try {
    const file = await readFile(tbSubjectFile, 'utf8')
    const results = await parseCsv(file)
    await prisma.deleteManyTbSubjects()
    for (const value of results.data) {
      if(value[0]==="tb_show"){
        continue
      }
      try {
        const tbSubject = await prisma
          .createTbSubject({
            show: value[0],
            subject: value[1],
            direction: value[2],
            order: parseInt(value[3]),
          })
        console.log(tbSubject);
      } catch (err) {
        console.log(err)
        continue
      }
    }
  } catch (err) {
    console.log(err);
  }
}

// 添加科目对照表信息

async function addSubjectContrast() {
  try {
    const file = await readFile(subjectContrastFile, 'utf8')
    const results = await parseCsv(file)
    await prisma.deleteManySubjectContrasts()
    for (const value of results.data) {
      if(value[0]==="origin"){
        continue
      }
      try {
        const subjectContrast = await prisma
          .createSubjectContrast({
            origin: value[0],
            tb: value[1],
            fs: value[2],
            coefficient: parseInt(value[3]),
            direction: value[4],
            firstClass:value[5],
            secondClass:value[6]
          })
        console.log(subjectContrast);
      } catch (err) {
        console.log(err)
        continue
      }
    }
  } catch (err) {
    console.log(err);
  }
}

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

// 添加标准会计科目信息

async function addStdSubject() {
  try {
    const file = await readFile(stdSubjectFile, 'utf8')
    const results = await parseCsv(file)
    await prisma.deleteManyStdSubjects()
    for (const value of results.data) {
      try {
        
        const stdSubject = await prisma
          .createStdSubject({
            code: value[0],
            name: value[1],
          })
        console.log(stdSubject);
      } catch (err) {
        console.log(err)
        continue
      }
    }
  } catch (err) {
    console.log(err);
  }
}

// addFs(fs2019File,"2019已执行三个新准则")
// addFs(fs2018File,"2019未执行三个新准则")
addTbSubject()
addSubjectContrast()
// addAccountingFirm()
// addStdSubject()