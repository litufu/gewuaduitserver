# -*- coding:utf-8 -*-

import sys
import requests
import pandas as pd


def get_rate(currency_type,date):
    '''
    获取人民币中间价
    :param currency_type:
    :param date:
    :return:
    '''
    r = requests.get("https://www.kuaiyilicai.com/bank/rmbfx/b-safe.html?querydate={}".format(date))
    dfs = pd.read_html(r.text)
    df = dfs[0]
    df = df[["币种","中间价"]]
    df = df.rename(columns={"币种":"currency_type","中间价":"price"})
    df = df[df["currency_type"].str.contains(currency_type)]
    values = df["price"].values
    if len(values)>0:
        return str(values[0])
    return "未找到"


if __name__ == '__main__':
    currency_type = sys.argv[1]
    date = sys.argv[2]
    # currency_type="美元"
    # date="2018-12-31"
    res = get_rate(currency_type, date)
    sys.stdout.write(res)