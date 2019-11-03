# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import LetterOfProofSetting

def add_or_update_letter_of_proof_setting(session,start_time,end_time,customer_amount,customer_balance,supplier_amount,supplier_balance,other_balance):
    '''
    添加或修改函证设置
    :param session:
    :param start_time:
    :param end_time:
    :param customer_amount:
    :param customer_balance:
    :param supplier_amount:
    :param supplier_balance:
    :param other_balance:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    settings = session.query(LetterOfProofSetting).filter(
        LetterOfProofSetting.start_time == start_time,
        LetterOfProofSetting.end_time == end_time,
    ).all()
    if len(settings) > 0:
        settings[0].customer_amount=customer_amount
        settings[0].customer_balance=customer_balance
        settings[0].supplier_amount=supplier_amount
        settings[0].supplier_balance=supplier_balance
        settings[0].other_balance=other_balance
        session.commit()
    else:
        setting = LetterOfProofSetting(
            start_time=start_time,
            end_time=end_time,
            customer_amount=customer_amount,
            customer_balance=customer_balance,
            supplier_amount=supplier_amount,
            supplier_balance=supplier_balance,
            other_balance=other_balance,
        )
        session.add(setting)
        session.commit()



if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    customer_amount = float(sys.argv[4])
    customer_balance = float(sys.argv[5])
    supplier_amount = float(sys.argv[6])
    supplier_balance = float(sys.argv[7])
    other_balance = float(sys.argv[8])
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    add_or_update_letter_of_proof_setting(session,start_time, end_time, customer_amount, customer_balance, supplier_amount,
                                          supplier_balance, other_balance)
    sys.stdout.write("success")