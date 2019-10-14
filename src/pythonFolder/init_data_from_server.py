#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base,FSSubject,SubjectContrast,TBSubject
import time
from utils import get_session_and_engine

sys.stdin.reconfigure(encoding='utf-8')

def add_fs_subject(session,lines):
    '''
    添加报表标准项目/TB标准科目/科目对照表
    :return:
    '''
    # 处理科目对照表：科目余额表=》TB=>报表之间的对应关系
    print(lines[1].strip()[:200])
    
    subject_contrasts = json.loads(lines[1].strip())
    # 科目对照表
    tb_subjects = json.loads(lines[2].strip())
    # 报表对照表
    fs_subjects = json.loads(lines[3].strip())

    # 删除对照表
    for obj in session.query(SubjectContrast).all():
        session.delete(obj)
    session.commit()

    for item in subject_contrasts:
        print(item)
        origin_subject = item["origin"]
        tb_subject = item["tb"]
        fs_subject = item["fs"]
        coefficient = item["coefficient"]
        direction = item["direction"]
        first_class = item["firstClass"]
        second_class = item["secondClass"]
        subjectcontrast = SubjectContrast(origin_subject=origin_subject,tb_subject=tb_subject,fs_subject=fs_subject,
                        coefficient=coefficient,direction=direction,first_class=first_class,second_class=second_class
                        )
        session.add(subjectcontrast)
    session.commit()
    # 删除TB对照表
    for obj in session.query(TBSubject).all():
        session.delete(obj)
    session.commit()
    # TB对照表   
    for item in tb_subjects:
        print(item)
        show = item["show"]
        subject = item["subject"]
        direction = item["direction"]
        order = item["order"]
        tbsubject = TBSubject(show=show,subject=subject,direction=direction,order=order)
        session.add(tbsubject)
    session.commit()
    # 添加报表对照项目
    # 删除报表对照表
    for obj in session.query(FSSubject).all():
        session.delete(obj)
    session.commit()
    for item in fs_subjects:
        print(item)
        name = item["name"]
        show = item["show"]
        subject = item["subject"]
        direction = item["direction"]
        fssubject = FSSubject(name=name,show=show, subject=subject, direction=direction)
        session.add(fssubject)
    session.commit()
        


# def add_first_class_subject(session):
#     df = pd.read_csv(first_clsss_subject_path)
#     for i in range(len(df)):
#         code = str(df.iat[i,0])
#         name = df.iat[i,1]
#         print(code)
#         print(name)
#         subject = FirstClassSubject(code=code,name=name)
#         session.add(subject)
#     session.commit()


def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('gbk')

if __name__ == '__main__':
    # db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    lines = sys.stdin.readlines()
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(json.loads(lines[0].strip())))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    add_fs_subject(session,lines)
    # add_first_class_subject(session)
    print("success")
    # get_account_firm(session)

