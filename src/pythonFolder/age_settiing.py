# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AgeSetting


def age_setting(session,start_time,end_time,years,months,one_year):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')

    age_settings = session.query(AgeSetting).filter(
        AgeSetting.start_time == start_time,
        AgeSetting.end_time == end_time,
    ).all()
    if len(age_settings) == 1:
        setting = age_settings[0]
        setting.years = years
        setting.months = months
        setting.one_year = one_year
        session.commit()
        sys.stdout.write("success")
    elif len(age_settings) == 0:
        setting = AgeSetting(
            start_time=start_time,
            end_time=end_time,
            years=years,
            months=months,
            one_year=one_year,
        )
        session.add(setting)
        session.commit()
        sys.stdout.write("success")
    else:
        raise Exception("age_settings错误")


if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    years = int(sys.argv[4])
    months = int(sys.argv[5])
    one_year = True if sys.argv[6] == "true"  else False
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # years=3
    # one_year=True
    # months=4
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    age_setting(session, start_time, end_time, years, months, one_year)