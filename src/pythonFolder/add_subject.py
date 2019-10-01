# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SubjectBalance


def add_subject(session,start_time,end_time,record):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    subjectInfo = json.loads(record)
    subject_num = subjectInfo.get("subjectNum","")
    subject_name = subjectInfo.get("subjectName","")
    subject_type = subjectInfo.get("subjectType","资产")
    direction = subjectInfo.get("direction", "借")
    is_specific = subjectInfo.get("isSpecific",True)
    if is_specific==1:
        is_specific = True
    else:
        is_specific = False
    subject_gradation = subjectInfo.get("subjectGradation",1)
    # 从数据库读取科目余额表
    if subject_num=="":
        raise Exception("未输入科目编码")
    subjects = session.query(SubjectBalance).filter(
        SubjectBalance.start_time == start_time,
        SubjectBalance.end_time == end_time,
        SubjectBalance.subject_num==subject_num
    ).all()
    if len(subjects)>0:
        raise Exception("已经存在该科目编码")

    subject = SubjectBalance(
        start_time=start_time,
        end_time=end_time,
        subject_num=subject_num,
        subject_name=subject_name,
        subject_type=subject_type,
        direction=direction,
        is_specific=is_specific,
        subject_gradation=subject_gradation,
        initial_amount=0.00,
        debit_amount=0.00,
        credit_amount=0.00,
        terminal_amount=0.00
    )
    session.add(subject)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    add_subject(session,sys.argv[2],sys.argv[3],sys.argv[4])