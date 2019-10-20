# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary


def auxiliary(engine,start_time,end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # 从数据库读取科目余额表
    df_auxiliary = pd.read_sql(session.query(Auxiliary).filter(Auxiliary.start_time == start_time,
                                                     Auxiliary.end_time == end_time,
                                                     ).statement, engine)
    sys.stdout.write(df_auxiliary.to_json(orient='records'))


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    auxiliary(engine,sys.argv[2],sys.argv[3])
