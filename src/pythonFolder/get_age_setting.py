# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AgeSetting

def get_age_setting(session,start_time,end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # 从数据库读取科目余额表
    age_settings = session.query(AgeSetting).filter(AgeSetting.start_time==start_time,AgeSetting.end_time==end_time).all()
    if len(age_settings) == 1:
        setting = {"months":age_settings[0].months,"years":age_settings[0].years,"oneYear":age_settings[0].one_year}
        sys.stdout.write(json.dumps(setting))
    else:
        setting = {"months": 4, "years": 3,"oneYear": True}
        sys.stdout.write(json.dumps(setting))



if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    get_age_setting(session,start_time,end_time)
