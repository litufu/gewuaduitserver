# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary


def add_subject(session,start_time,end_time,record):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    auxiliaryInfo = json.loads(record)
    subject_num = auxiliaryInfo.get("subjectNum","")
    subject_name = auxiliaryInfo.get("subjectName","")
    type_num = auxiliaryInfo.get("typeNum","")
    type_name = auxiliaryInfo.get("typeName","")
    code = auxiliaryInfo.get("code","")
    name = auxiliaryInfo.get("name","")
    direction = auxiliaryInfo.get("direction", "借")
    # 从数据库读取辅助核算明细
    if name=="":
        raise Exception("未输入辅助核算名称")
    auxiliaries = session.query(Auxiliary).filter(
        Auxiliary.start_time == start_time,
        Auxiliary.end_time == end_time,
        Auxiliary.name==name
    ).all()
    if len(auxiliaries)>0:
        raise Exception("已经存在该辅助核算项目")

    auxiliary = Auxiliary(
        start_time=start_time,
        end_time=end_time,
        subject_num=subject_num,
        subject_name=subject_name,
        type_num=type_num,
        type_name=type_name,
        code=code,
        name=name,
        direction=direction,
        initial_amount=0.00,
        debit_amount=0.00,
        credit_amount=0.00,
        terminal_amount=0.00
    )
    session.add(auxiliary)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    add_subject(session,sys.argv[2],sys.argv[3],sys.argv[4])