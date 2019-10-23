# -*- coding:utf-8 -*-

import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AduitAdjustment


def aduit_adjustment(session,end_time,vocher_num,vocher_type="审"):
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    aduit_adjustments = session.query(AduitAdjustment).filter(AduitAdjustment.year==end_time.year,AduitAdjustment.month==end_time.month,AduitAdjustment.vocher_num==vocher_num,AduitAdjustment.vocher_type==vocher_type).all()
    for aduit_adjustment in aduit_adjustments:
        session.delete(aduit_adjustment)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    end_time = sys.argv[2]
    vocher_num = sys.argv[3]
    vocher_type = sys.argv[4]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    aduit_adjustment(session,end_time,vocher_num,vocher_type)
