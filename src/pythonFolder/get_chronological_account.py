# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import  check_start_end_date


def append_all_gradation_subjects(df_km, df_xsz):
    '''
    为序时账添加所有级别的会计科目编码和名称
    :param df_km: 科目余额表
    :param df_xsz: 序时账
    :return: 添加过所有级别会计科目编码和名称的序时账
    '''
    # 添加科目编码长度列
    df_km = df_km.copy()
    df_xsz = df_xsz.copy()

    df_km['subject_length'] = df_km['subject_num'].str.len()
    df_km_subject = df_km[['subject_num', 'subject_name']]
    df_km_subject = df_km_subject.rename({'subject_num': 'std_subject_num'}, axis='columns')
    # 获取各科目级次和长度
    df_km_gradation = df_km.drop_duplicates('subject_gradation', keep='first')
    df_km_gradation = df_km_gradation[['subject_gradation', 'subject_length']].sort_values(by="subject_length")
    # 给序时账添加所有的科目级别编码和科目名称
    gradation_subject_and_length = list(zip(df_km_gradation['subject_gradation'], df_km_gradation['subject_length']))
    for i in range(len(gradation_subject_and_length)):
        subject_num_length = gradation_subject_and_length[i][1]
        subject_num_name = 'subject_num_{}'.format(i + 1)
        df_xsz[subject_num_name] = df_xsz['subject_num'].str.slice(0, subject_num_length)
        df_xsz = pd.merge(df_xsz, df_km_subject, how='left', left_on=subject_num_name, right_on="std_subject_num",
                          suffixes=('', '_{}'.format(i + 1)))
        df_xsz = df_xsz.drop(columns=['std_subject_num'])
    return df_xsz

def chronological_account(engine,start_time,end_time,subject_num,grade):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)
    # 从数据库读取科目余额表
    df_km = pd.read_sql_table('subjectbalance', engine)
    df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]

    year = start_time.year
    start_month = start_time.month
    end_month = end_time.month
    df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    df_xsz = df_xsz[(df_xsz['year'] == year) & (df_xsz['month'] >= start_month) & (df_xsz['month'] <= end_month)]
    # 为序时账添加所有级别的会计科目编码和名称
    df_xsz = append_all_gradation_subjects(df_km, df_xsz)
    subject_num_grade = "subject_num_{}".format(grade)
    df_xsz_new = df_xsz[df_xsz[subject_num_grade]==subject_num]
    df_xsz_new = df_xsz_new[["year","month","vocher_type","vocher_num","subentry_num","description","subject_num","subject_name","debit","credit","auxiliary"]]
    sys.stdout.write(df_xsz_new.to_json(orient='records'))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    chronological_account(engine,sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
