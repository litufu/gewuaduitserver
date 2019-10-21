# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AccountAge


def get_current_account_age(engine,session,start_time,end_time):
    '''
    将往来款的发生时间放在数据库
    :param engine:
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df = pd.read_sql(session.query(AccountAge).filter(AccountAge.start_time==start_time,AccountAge.end_time==end_time).statement,engine)
    sys.stdout.write(df.to_json(orient='records'))



if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    get_current_account_age(engine,session,start_time,end_time)

