# -*- coding:utf-8 -*-

import sys
import os
import random
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import io
import json
from utils import replace_brace


cookies_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'settings','qichacha_cookies.txt')

# 设置企查查爬虫headers
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}


def get_cookies():
    # 将cookies字符串转化为dict
    f = open(cookies_path, 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    lines = f.readlines()
    choice = random.randint(0,len(lines)-1)
    content = lines[choice]
    for line in content.split(';'):  # 按照字符：进行划分读取
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
        if replace_brace(company_name) == replace_brace(a.get_text().strip()):
            href = a['href']
            return href
    return ""



def get_company_info(soup,company_name,ipo):
    '''
    获取公司基本信息
    :param soup: beautifulsoup对象
    :param company_name: 公司名称
    :return: company对象
    '''
    if ipo:
        # （1）获取注册资本
        pattern1 = re.compile("注册资本")
        element1 = soup.find(text=pattern1).parent.find_next_sibling("td")
        registered_capital = element1.text.strip()
        # （1.2）获取实缴资本
        padin_capital = registered_capital
        # （2）获取成立日期
        pattern2 = re.compile("成立日期")
        element2 = soup.find(text=pattern2).parent.find_next_sibling("td")
        establish_date = element2.text.strip()
        # （3）获取经营范围
        theme = soup.find(id="ipoTheme")
        element3 = theme.find('table')
        business_scope = element3.text.strip()
        # （4）获取企业信用编码
        pattern4 = re.compile("工商登记")
        element4 = soup.find(text=pattern4).parent.find_next_sibling("td")
        code = element4.text.strip()
        # (5)获取企业地址
        pattern5 = re.compile("办公地址")
        element5 = soup.find(text=pattern5).parent.find_next_sibling("td")
        address = element5.text.strip()
        # 获取企业法定代表人
        pattern6 = re.compile("法人代表")
        element6 = soup.find(text=pattern6).parent.find_next_sibling("td")
        legal_representative = element6.text.strip()
        company = {"name": company_name, "code": code, "address": address, "legalRepresentative": legal_representative,
                   "establishDate": establish_date, "registeredCapital": registered_capital,
                   "paidinCapital": padin_capital, "businessScope": business_scope
                   }
    else:
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
    return company


def get_company_holders(soup,ipo):
    if ipo:
        # 获取网页中股东部分
        partners = soup.find(id="gdList")
        if partners is None:
            return
        # 获取股东表格
        table = partners.find('table')
        if table is None:
            return
        # 处理股东表格，使得其成为标准的html的table格式
        # 去除掉表头的a标签
        for th in table.find_all('th'):
            a_tags = th.find_all('a')
            for a_tag in a_tags:
                a_tag.replace_with('')
        # 去除掉单元格中的表格，用表格中的h3标签内容代替
        for tab in table.find_all('table'):
            h3 = tab.find('h3')
            if h3:
                if h3.string:
                    tab.replace_with(h3.string)
                else:
                    tab.replace_with("")
            else:
                tab.replace_with("")
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
                split_spaces = text.split(' ')
                if len(split_spaces)>1:
                    text = split_spaces[0].strip()
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
            "发起人及出资信息": "holder_name",
            "股东名称":"holder_name",
            "合伙人信息": "holder_name",
            "持股比例": "ratio",
        })
        df = df[['holder_name', 'ratio']]
    else:
        # 获取网页中股东部分
        partners = soup.find(id="partnerslist")
        if partners is None:
            return
        # 获取股东表格
        table = partners.find('table')
        if table is None:
            return
        # 处理股东表格，使得其成为标准的html的table格式
        # 去除掉表头的a标签
        for th in table.find_all('th'):
            a_tags = th.find_all('a')
            for a_tag in a_tags:
                a_tag.replace_with('')
        # 去除掉单元格中的表格，用表格中的h3标签内容代替
        for tab in table.find_all('table'):
            h3 = tab.find('h3')
            if h3:
                if h3.string:
                    tab.replace_with(h3.string)
                else:
                    tab.replace_with("")
            else:
                tab.replace_with("")
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
            "发起人及出资信息": "holder_name",
            "合伙人信息": "holder_name",
            "持股比例": "ratio",
            "认缴出资额": "promise_to_pay_amount",
            "认缴出资日期": "promise_to_pay_date",
            "实缴出资额": "pay_amount",
            "实缴出资日期": "pay_date",
        })
        df = df[['holder_name', 'ratio']]
    return json.loads(df.to_json(orient='records'))



def get_main_members(soup,ipo):
    if ipo:
        # 获取网页中主要成员部分
        members = soup.find(id="ggList")
        if members is None:
            return
        # 获取股东表格
        tables = members.find_all('table')
        if tables is None:
            return
        # 处理主要成员表格，使得其成为标准的html的table格式
        dfs = []
        for table in tables:
            # 去除掉表头的a标签
            for th in table.find_all('th'):
                a = th.find('a')
                if a:
                    a.replace_with('')
            # 用表格中的h3标签内容代替
            for td in table.find_all('td'):
                h3 = td.find('h3')
                if h3:
                    td.string = h3.string
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
                "姓名": "name",
                "职务": "post",
            })
            df = df[['name', 'post']]
            dfs.append(df)
        df = pd.concat(dfs,ignore_index=True)
    else:
        # 获取网页中主要成员部分
        members = soup.find(id="Mainmember")
        if members is None:
            return
        # 获取股东表格
        table = members.find('table')
        if table is None:
            return
        # 处理主要成员表格，使得其成为标准的html的table格式
        # 去除掉表头的a标签
        for th in table.find_all('th'):
            a = th.find('a')
            if a:
                a.replace_with('')
        # 用表格中的h3标签内容代替
        for td in table.find_all('td'):
            h3 = td.find('h3')
            if h3:
                td.string = h3.string
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
            "姓名": "name",
            "职务": "post",
        })
        df = df[['name', 'post']]
    return json.loads(df.to_json(orient='records'))


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
        sys.stdout.write(json.dumps({"name": company_name}))
        sys.stdout.flush()
        return
    origin_url = 'https://www.qichacha.com'
    # 请求详情页面
    r = requests.get(origin_url + url, headers=headers)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    # 检查是否为上市公司 如果是上市公司，则按照上市公司的格式获取信息
    ipoBase = soup.find(id="ipoBase")
    ipo = True if ipoBase else False
    # 获取公司基本信息
    try:
        company_info = get_company_info(soup,company_name,ipo)
        company_holders = get_company_holders(soup,ipo)
        main_members = get_main_members(soup,ipo)
        res = {"companyInfo":company_info,"holders":company_holders,"members":main_members}
        sys.stdout.write(json.dumps(res))
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(json.dumps({"name":company_name}))
        sys.stdout.flush()
        return
  

if __name__ == "__main__":
    company_name = sys.argv[1]
    download_company(company_name)
    # download_company("深圳市众恒世讯科技股份有限公司")
