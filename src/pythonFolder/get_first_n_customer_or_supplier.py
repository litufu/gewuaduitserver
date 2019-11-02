# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import CustomerAnalysis,SupplierAnalysis

def get_first_company(session,engine,start_time,end_time,num,type):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')

    if type=="customer":
        df = pd.read_sql(session.query(CustomerAnalysis).filter(CustomerAnalysis.start_time==start_time,CustomerAnalysis.end_time==end_time).statement,engine)
        df = df.sort_values(by='sale_amount', ascending=False)
        df = df[["name","sale_amount"]]
    elif type == "supplier":
        df = pd.read_sql(session.query(SupplierAnalysis).filter(SupplierAnalysis.start_time == start_time,
                                                                SupplierAnalysis.end_time == end_time).statement,
                         engine)
        df = df.sort_values(by='purchase_amount', ascending=False)
        df = df[["name", "purchase_amount"]]
    else:
        raise Exception("类型错误")
    first_n_df = df[:num]
    return first_n_df




if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    num = int(sys.argv[4])
    type = sys.argv[5]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    first_n_df = get_first_company(session,engine,start_time,end_time,num,type)
    sys.stdout.write(first_n_df.to_json(orient='records'))