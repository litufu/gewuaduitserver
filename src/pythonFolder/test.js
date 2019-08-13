
const spawn = require("child_process").spawn;


function download_companyinfo(company_name){
    const bat = spawn('python',["download_companyinfo.py", company_name]);
    bat.stdout.on('data', (data) => {
        res = JSON.parse(data)
        if(Array.isArray(res)){
            console.log(res);
        }
    });
    
    bat.stderr.on('data', (data) => {
        console.log(data.toString());
    });


    bat.on('exit', (code) => {
        console.log(`子进程退出，退出码 ${code}`);
    });
}

download_companyinfo("安阳格物网络科技有限公司")