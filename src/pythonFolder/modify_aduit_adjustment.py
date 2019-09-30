# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AduitAdjustment


def modify_aduit_ajustment(session,start_time,end_time,record,vocher_num):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    records = json.loads(record)
    # 从数据库读取原来的分录,并删除
    aduit_adjustments = session.query(AduitAdjustment).filter(AduitAdjustment.record_time == end_time,AduitAdjustment.vocher_num==vocher_num).all()
    if len(aduit_adjustments)==0:
        raise Exception("未找到对应的分录")
    for aduit_adjustment in aduit_adjustments:
        session.delete(aduit_adjustment)
    session.commit()

    for i,record in enumerate(records):
        subject =record.get("subject","").split("_")
        if len(subject)==0:
            raise Exception("未录入科目")
        subject_num = subject[0]
        subject_name = subject[1]
        debit = float(record.get("debit",0.00))
        credit = float(record.get("credit",0.00))
        auxiliary=record.get("auxiliary","").split("_")
        if len(auxiliary)==4:
            auxiliaryDirection = "借" if abs(debit)>0.00 else "贷"
            auxiliaryAmount = debit if abs(debit)>0.00 else credit
            auxiliaryStr = "【{}: {} {}  {}】".format(auxiliary[2],auxiliary[3],auxiliaryDirection,auxiliaryAmount)
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
        vocher_num = aduit_adjustments[0].vocher_num
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
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    modify_aduit_ajustment(session,sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])