# -*- coding:utf-8 -*-

import sys
import pandas as pd
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import  check_start_end_date


def check_exists(subject_name,df_km):
    df_km_this_year_profit = df_km[df_km["subject_name"] == subject_name]
    if len(df_km_this_year_profit) > 0:
        return {"content": "检查{}科目是否存在".format(subject_name), "result": "存在"}
    else:
        return {"content": "检查{}科目是否存在".format(subject_name), "result": "不存在，请增加相关科目"}

def checke_profit_and_loss_carry_orver(engine,start_time,end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)
    # 从数据库读取科目余额表
    res = []
    df_km = pd.read_sql_table('subjectbalance', engine)
    df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]
    for item in ["本年利润","未分配利润","以前年度损益调整"]:
        result = check_exists(item,df_km)
        res.append(result)
    sys.stdout.write(json.dumps(res))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    checke_profit_and_loss_carry_orver(engine,sys.argv[2],sys.argv[3])
