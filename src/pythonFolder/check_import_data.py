# -*- coding:utf-8 -*-

import pandas as pd
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import str_to_float,check_start_end_date
from database import Auxiliary, SubjectBalance, ChronologicalAccount

def check_import_data(engine,start_time, end_time):
    '''
    检查科目余额表与序时账是否一致
    检查科目余额表与辅助核算明细表是否一致
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
    # 获取科目余额表
    df_km = pd.read_sql_table('subjectbalance', engine)
    df_km = df_km[(df_km['start_time']==start_time) & (df_km['end_time']==end_time) ]
    # 获取序时账
    df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    df_xsz = df_xsz[(df_xsz['year'] == year) & (df_xsz['month'] >= start_month) & (df_xsz['month'] <= end_month) ]
    # 获取辅助核算明细表
    df_hs = pd.read_sql_table('auxiliary', engine)
    df_hs = df_hs[
        (df_hs['start_time'] == start_time) & (df_hs['end_time'] == end_time)]
    # （1）检查序时账借贷方发生额与科目余额表是否一致
    # 获取科目余额表借贷方发生额
    df_km_slim = df_km[['subject_num','debit_amount','credit_amount']]
    df_km_subject = df_km_slim.set_index('subject_num')
    # 获取序时账数据透视表，合计为借贷方，索引为科目编码
    df_xsz_pivot = df_xsz.pivot_table(values=['debit', 'credit'], index='subject_num',  aggfunc='sum')
    # 合并两个表，并比较发生额是否一致
    df1 = pd.merge(df_xsz_pivot, df_km_subject, left_index=True, right_index=True, how='left')
    df1['credit_equal'] = df1['credit'] - df1['credit_amount'] < 0.001
    df1['debit_equal'] = df1['debit'] - df1['debit_amount'] < 0.001
    texts = []
    if not df1['credit_equal'].all():
        texts.append('科目余额表和序时账贷方合计不一致')
    if not df1['debit_equal'].all():
        texts.append('科目余额表和序时账借方合计不一致')
    #  （2）检查辅助核算明细表与科目余额表是否一致
    #     分别检查期初数/本期借方/本期贷方/期末数是否一致
    # 获取科目余额表期初数/本期借方/本期贷方/期末数
    if len(df_hs) > 0:
        df_km_slim2 = df_km[['subject_num','initial_amount', 'debit_amount', 'credit_amount','terminal_amount']]
        df_km_subject2 = df_km_slim2.set_index('subject_num')
        # 获取辅助核算数据透视表，合计为期初期末和借贷方，索引为科目编码
        df_hs_pivot = df_hs.pivot_table(values=['initial_amount', 'debit_amount','credit_amount','terminal_amount'],
                                        index=['subject_num','type_num'], aggfunc='sum')
        # 合并两个表，并比较发生额是否一致
        df2 = pd.merge(df_hs_pivot, df_km_subject2, left_index=True, right_index=True, how='left')
        df2['initial_equal'] = df2['initial_amount_x'] - df2['initial_amount_y'] < 0.001
        if not df2['initial_equal'].all():
            texts.append('科目余额表与辅助核算明细表期初数不一致')
        df2['credit_equal'] = df2['credit_amount_x'] - df2['credit_amount_y'] < 0.001
        if not df2['credit_equal'].all():
            texts.append('科目余额表与辅助核算明细表贷方发生额不一致')
        df2['debit_equal'] = df2['debit_amount_x'] - df2['debit_amount_y'] < 0.001
        if not df2['debit_equal'].all():
            texts.append('科目余额表与辅助核算明细表借方发生额不一致')
        df2['terminal_equal'] = df2['terminal_amount_x'] - df2['terminal_amount_y'] < 0.001
        if not df2['terminal_equal'].all():
            texts.append('科目余额表与辅助核算明细表期末数不一致')
    if len(texts)>0:
        sys.stdout.write(','.join(texts))
    else:
        sys.stdout.write("核对一致")

if __name__ == '__main__':
    # db_path = sys.argv[1]
    db_path = "D:\gewuaduit\db\cjz6d8rpd0nat0720w8yj2ave-ck2qvzkio000p0712cg33k9e9.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # start_time = sys.argv[2]
    # end_time = sys.argv[3]
    start_time = "2015-1-1"
    end_time = "2015-12-31"
    check_import_data(engine,start_time,end_time)