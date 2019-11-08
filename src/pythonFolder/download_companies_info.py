# -*- coding:utf-8 -*-

import sys
import time
import json
from download_companyinfo import download_company
import random

def download_all_companies_info(companies):
    i = 0
    for company in companies:
        i = i + 1
        download_company(company)
        time.sleep(5)
        if i>10:
            s = random.randint(1,4)
            time.sleep(60*s)
            i=0


if __name__ == '__main__':
    companyStr = sys.argv[1]
    companies = json.loads(companyStr)
    # companies = ["广东金贝尔通信科技有限公司","东莞市百镀通五金电镀实业有限公司","神宇通信科技股份公司","广州致远合金制品有限公司","深圳市联丰电子有限公司","丹阳市恒立电子有限公司","漳州新格有色金属有限公司","江苏亨鑫科技有限公司","东莞市勤鹏精密五金有限公司","哈博（常州）电缆有限公司","摩比天线技术（深圳）有限公司","摩比通讯技术（吉安）有限公司","苏州市永创金属科技有限公司","康普通讯技术（中国）有限公司","摩比科技（深圳）有限公司","北京天河鸿城电子有限责任公司","江苏亨鑫无线技术有限公司","东莞东山精密制造有限公司","摩比科技（西安）有限公司","易德龙电器有限公司"]
    download_all_companies_info(companies)
