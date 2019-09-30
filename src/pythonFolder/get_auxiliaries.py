# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def auxiliaries(engine,start_time,end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # 从数据库读取科目余额表
    df_km = pd.read_sql_table('auxiliary', engine)
    df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]
    df_km_new = df_km[['subject_num','subject_name','type_name', 'name']]
    sys.stdout.write(df_km_new.to_json(orient='records'))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    auxiliaries(engine,sys.argv[2],sys.argv[3])
