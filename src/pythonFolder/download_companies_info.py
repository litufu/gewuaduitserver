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
    download_all_companies_info(companies)
