# -*- coding:utf-8 -*-

import pandas as pd
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import str_to_float,check_start_end_date
from database import Auxiliary, SubjectBalance, ChronologicalAccount


def get_chronological_account_pivot(engine,session,start_time, end_time):
    '''
    获取序时账透视表
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)
    year = start_time.year
    start_month = start_time.month
    end_month = end_time.month
    df_xsz = pd.read_sql(session.query(ChronologicalAccount).filter(ChronologicalAccount.year==year,ChronologicalAccount.month>=start_month,ChronologicalAccount.month<=end_month).statement,engine)
    # 获取序时账数据透视表，合计为借贷方，索引为科目编码
    df_xsz_pivot = df_xsz.pivot_table(values=['debit', 'credit'], index='subject_num', aggfunc='sum')
    df_xsz_pivot = df_xsz_pivot.reset_index()
    return df_xsz_pivot



if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\db\cjz6d8rpd0nat0720w8yj2ave-ck2qvzkio000p0712cg33k9e9.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # start_time = "2015-1-1"
    # end_time = "2015-12-31"
    df_xsz_pivot = get_chronological_account_pivot(engine,session,start_time,end_time)
    sys.stdout.write(df_xsz_pivot.to_json(orient='records'))