# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AduitAdjustment


def aduit_ajustment(session,start_time,end_time,record):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    records = json.loads(record)
    # 从数据库读取科目余额表
    aduit_adjustments = session.query(AduitAdjustment).filter(AduitAdjustment.record_time == end_time).all()
    for i,record in enumerate(records):
        subject =record.get("subject","").split("_")
        if len(subject)==0:
            raise Exception("未录入科目")
        subject_num = subject[0]
        subject_name = subject[1]
        debit = float(record.get("debit",0.00))
        credit = float(record.get("credit",0.00))
        auxiliary=record.get("auxiliary","").split("_")
        if len(auxiliary)==2:
            auxiliaryDirection = "借" if abs(debit)>0.00 else "贷"
            auxiliaryAmount = debit if abs(debit)>0.00 else credit
            auxiliaryStr = "【{}: {} {}  {}】".format(auxiliary[0],auxiliary[1],auxiliaryDirection,auxiliaryAmount)
        else:
            auxiliaryStr = ""
        foreign_currency = record.get("foreign_currency", 0.00)
        if foreign_currency=="":
            foreign_currency = 0.00
        if abs(debit) >0.00:
            debit_foreign_currency=float(foreign_currency)
            credit_foreign_currency=0.00
        else:
            debit_foreign_currency = 0.00
            credit_foreign_currency = float(foreign_currency)
        if len(aduit_adjustments)>0:
            vocher_num = aduit_adjustments[-1].vocher_num + 1
        else:
            vocher_num = 1
        aduit_adjustment = AduitAdjustment(
            year=start_time.year,
            month=end_time.month,
            record_time=end_time,
            vocher_type="审",
            vocher_num=vocher_num,
            subentry_num=i+1,
            description=record.get("description",""),
            subject_num=subject_num,
            subject_name=subject_name,
            currency_type=record.get("currency_type",""),
            debit=debit,
            credit=credit,
            debit_foreign_currency=debit_foreign_currency,
            credit_foreign_currency=credit_foreign_currency,
            debit_number=0.00,
            credit_number=0.00,
            debit_price=0.00,
            credit_price=0.00,
            auxiliary=auxiliaryStr
        )
        session.add(aduit_adjustment)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # record = "[{\"description\":\"确认收入\",\"subject\":\"112201_人民币\",\"currency_type\":\"RMB\",\"foreign_currency\":\"\",\"debit\":\"1130\",\"credit\":0,\"auxiliary\":\"112201_人民币_客户_康普通讯科技(上海)有限公司\",\"tableData\":{\"id\":0}},{\"currency_type\":\"RMB\",\"foreign_currency\":\"0\",\"debit\":\"0\",\"credit\":\"1000\",\"description\":\"确认收入\",\"subject\":\"6001_主营业务收入\",\"tableData\":{\"id\":1}},{\"currency_type\":\"RMB\",\"foreign_currency\":\"0.00\",\"debit\":\"0.00\",\"credit\":\"130\",\"description\":\"确认收入\",\"subject\":\"22210105_销项税款\",\"tableData\":{\"id\":2}}]"

    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # aduit_ajustment(session,start_time,end_time,record)
    aduit_ajustment(session,sys.argv[2],sys.argv[3],sys.argv[4])