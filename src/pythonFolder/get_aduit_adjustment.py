# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def aduit_adjustment(engine,end_time):
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # 从数据库读取科目余额表
    df_adjustment = pd.read_sql_table('aduitadjustment', engine)
    df_adjustment = df_adjustment[(df_adjustment['record_time'] == end_time)&(df_adjustment['vocher_type'] == "审")]
    df_adjustment_new = df_adjustment[['vocher_num',"subentry_num",'description','subject_num','subject_name', 'debit',"credit","auxiliary"]]
    sys.stdout.write(df_adjustment_new.to_json(orient='records'))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    aduit_adjustment(engine,sys.argv[2])
