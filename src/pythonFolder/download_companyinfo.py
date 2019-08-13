# -*- coding:utf-8 -*-

import sys
import os 
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import io
from datetime import datetime
import json

cookies_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'settings','qichacha_cookies.txt')

# 设置企查查爬虫headers
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
}


def get_cookies():
    # 将cookies字符串转化为dict
    f = open(cookies_path, 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    for line in f.read().split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    return cookies


def get_company_detail_url(company_name):
    # 获取公司企查查详情页url
    payload = {'key': company_name}
    cookies = get_cookies()
    origin_url = 'https://www.qichacha.com/search'
    r = requests.get(origin_url, params=payload, headers=headers, cookies=cookies)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    trs = soup.find_all("tr")
    for tr in trs:
        a = tr.find(href=re.compile("firm"))
        if company_name == a.get_text():
            href = a['href']
            return href
    return ""


def get_company_info(soup,company_name):
    '''
    获取公司基本信息
    :param soup: beautifulsoup对象
    :param company_name: 公司名称
    :return: company对象
    '''

    # （1）获取注册资本
    pattern1 = re.compile("注册资本")
    element1 = soup.find(text=pattern1).parent.find_next_sibling("td")
    registered_capital = element1.text.strip()
      # （1.2）获取实缴资本	
    pattern12 = re.compile("实缴资本")
    element12 = soup.find(text=pattern12).parent.find_next_sibling("td")
    padin_capital = element12.text.strip()
    # （2）获取成立日期
    pattern2 = re.compile("成立日期")
    element2 = soup.find(text=pattern2).parent.find_next_sibling("td")
    establish_date = element2.text.strip()
    # （3）获取经营范围
    pattern3 = re.compile("经营范围")
    element3 = soup.find(text=pattern3).parent.find_next_sibling("td")
    business_scope = element3.text.strip()
    # （4）获取企业信用编码
    pattern4 = re.compile("统一社会信用代码")
    element4 = soup.find(text=pattern4).parent.find_next_sibling("td")
    code = element4.text.strip()
    # (5)获取企业地址
    pattern5 = re.compile("企业地址")
    element5 = soup.find(text=pattern5).parent.find_next_sibling("td")
    # 移除查看地图和附近企业两个标签
    for link in element5.find_all('a'):
        link.replace_with('')
    address = element5.text.strip()
    # 获取企业法定代表人
    element6 = soup.find(attrs={"class": "bname"})
    legal_representative = element6.text.strip()
    company = {"name":company_name,"code":code,"address":address,"legalRepresentative":legal_representative,
        "establishDate":establish_date,"registeredCapital":registered_capital,"paidinCapital":padin_capital,"businessScope":business_scope
    }
    company_string = json.dumps(company)
    print(company_string)
    sys.stdout.flush()
    
    


def get_company_holders(soup,company_name):
    # 获取网页中股东部分
    partners = soup.find("section", id="partnerslist")
    if partners is None:
        return
    # 获取股东表格
    table = partners.find('table')
    if table is None:
        return
    # 处理股东表格，使得其成为标准的html的table格式
    # 去除掉表头的a标签
    for th in table.find_all('th'):
        a = th.find('a')
        if a:
            a.replace_with('')
    # 去除掉单元格中的表格，用表格中的h3标签内容代替
    for tab in table.find_all('table'):
        name = tab.find('h3').string
        tab.replace_with(name)
    # 获取表格中所有的行
    rows = table.find_all('tr')
    # 利用StringIO制作df
    csv_io = io.StringIO()
    for row in rows:
        row_texts = []
        for cell in row.findAll(['th', 'td']):
            text = cell.get_text().strip()
            text = text.replace(',', '')
            res = text.split('\n')
            if len(res) > 1:
                text = res[0].strip()
            row_texts.append(text)
        row_string = ','.join(row_texts) + '\n'
        csv_io.write(row_string)
    csv_io.seek(0)
    df = pd.read_csv(csv_io)
    pattern = re.compile(r'(.*)[\(（].*?')
    df = df.rename(index=str, columns=lambda x: re.match(pattern, x)[1] if re.match(pattern, x) else x)
    df = df.rename(index=str, columns={
        "序号": "no",
        "股东及出资信息": "holder_name",
        "持股比例": "ratio",
        "认缴出资额": "promise_to_pay_amount",
        "认缴出资日期": "promise_to_pay_date",
        "实缴出资额": "pay_amount",
        "实缴出资日期": "pay_date",
    })
    df = df[['holder_name', 'ratio']]
    print(df.to_json(orient='records'))
    sys.stdout.flush()
 


def download_company(company_name):
    '''
    下载公司基本信息和股东信息
    :param company_name:公司名称
    :return:None
    '''
   
    #  没有存储则到企查查爬取
    #  获取详情页页面
    url = get_company_detail_url(company_name)
    if url.isspace():
        print("")
    origin_url = 'https://www.qichacha.com'
    # 请求详情页面
    r = requests.get(origin_url + url, headers=headers)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    # 获取公司基本信息
    try:
        get_company_info(soup,company_name)
        get_company_holders(soup,company_name)
    except Exception as e:
        print("")
        raise Exception("下载公司失败,{}".format(e))
  

if __name__ == "__main__":
    download_company(sys.argv[1])