# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import LetterOfProofSetting


def get_letter_of_proof_setting(session,start_time,end_time):
    '''
    获取函证设置
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    settings = session.query(LetterOfProofSetting).filter(LetterOfProofSetting.start_time==start_time,LetterOfProofSetting.end_time==end_time).all()
    if len(settings)>0:
        res = {
            "customerAmount":settings[0].customer_amount,
            "customerBalance":settings[0].customer_balance,
            "supplierAmount":settings[0].supplier_amount,
            "supplierBalance":settings[0].supplier_balance,
            "otherBalance":settings[0].other_balance,
        }
        return res
    else:
        res = {
            "customerAmount": 60,
            "customerBalance":60,
            "supplierAmount": 60,
            "supplierBalance": 60,
            "otherBalance": 60,
        }
        return res


if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # db_path = "D:\gewuaduit\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    res = get_letter_of_proof_setting(session,start_time,end_time)
    sys.stdout.write(json.dumps(res))