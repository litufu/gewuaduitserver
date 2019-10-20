# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary

def get_customer_and_supplier_same_company(session,start_time,end_time):
    '''
    获取即为客户又为供应商的单位
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df = pd.read_sql(session.query(Auxiliary).filter(Auxiliary.start_time == start_time,
                                                     Auxiliary.end_time == end_time,
                                                            ).statement, engine)
    df_customers = df[df["type_name"].str.contains("客户")].drop_duplicates("name")
    df_suppliers = df[df["type_name"].str.contains("供应商")].drop_duplicates("name")
    names = list(set(df_customers["name"].to_list()).intersection(set(df_suppliers["name"].to_list())))
    sys.stdout.write(json.dumps(names))



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
    get_customer_and_supplier_same_company(session,start_time,end_time)