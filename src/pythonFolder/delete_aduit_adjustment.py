# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AduitAdjustment


def aduit_adjustment(session,end_time,vocher_num):
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    aduit_adjustments = session.query(AduitAdjustment).filter(AduitAdjustment.record_time==end_time,AduitAdjustment.vocher_num==vocher_num,AduitAdjustment.vocher_type=="审").all()
    for aduit_adjustment in aduit_adjustments:
        session.delete(aduit_adjustment)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    aduit_adjustment(session,sys.argv[2],sys.argv[3])
