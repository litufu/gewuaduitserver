# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def changeReasons(engine,start_time,end_time,statement,audit):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # 从数据库读取科目余额表
    df_change = pd.read_sql_table('changereason', engine)
    df_change = df_change[(df_change['start_time'] == start_time) &
                  (df_change['end_time'] == end_time) &
                  (df_change['statement'] == statement) &
                  (df_change['audit'] == audit)
    ]
    df_change_new = df_change[['order', 'reason']]
    sys.stdout.write(df_change_new.to_json(orient='records'))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    changeReasons(engine,sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
