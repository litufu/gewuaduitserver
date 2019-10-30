# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary
from get_first_n_customer_or_supplier import get_first_company



def get_customer_and_supplier_names(session,engine,start_time,end_time,num):
    '''
    获取前10大客户和供应商的工商信息
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''


    suppliers = get_first_company(session,engine,start_time,end_time,num,"supplier")
    customers = get_first_company(session,engine,start_time,end_time,num,"customer")

    companies = [*suppliers,*customers]
    # auxiliaries = session.query(Auxiliary).filter(Auxiliary.start_time==start_time,Auxiliary.end_time==end_time).all()
    # for auxiliary in auxiliaries:
    #     if ("客户" in auxiliary.type_name) or ("供应商" in auxiliary.type_name):
    #         companies.append(auxiliary.name)
    return companies

if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    num = int(sys.argv[4])
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    companies = get_customer_and_supplier_names(session,engine, start_time, end_time,num)
    sys.stdout.write(json.dumps(companies))