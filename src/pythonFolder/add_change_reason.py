# -*- coding:utf-8 -*-

import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import ChangeReason


def add_change_reason(session,start_time,end_time,record):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    changeReasonInfo = json.loads(record)
    statement = changeReasonInfo.get("statement","")
    audit = changeReasonInfo.get("audit","")
    order = changeReasonInfo.get("order","")
    reason = changeReasonInfo.get("reason", "")
    # 从数据库读取科目余额表
    if reason=="":
        raise Exception("未输入科目变动原因")
    changeReasons = session.query(ChangeReason).filter(
        ChangeReason.start_time == start_time,
        ChangeReason.end_time == end_time,
        ChangeReason.statement==statement,
        ChangeReason.audit==audit,
        ChangeReason.order==order,
    ).all()
    if len(changeReasons)>0:
        for changeReason in changeReasons:
            session.delete(changeReason)
        session.commit()
    changeReason = ChangeReason(
        start_time=start_time,
        end_time=end_time,
        statement=statement,
        audit=audit,
        order=order,
        reason=reason,
    )
    session.add(changeReason)
    session.commit()
    sys.stdout.write("success")


if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # record="{\"statement\":\"资产负债表\",\"audit\":\"未审\",\"order\":103,\"reason\":\"你们好\"}"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # add_change_reason(session,start_time,end_time,record)
    add_change_reason(session,sys.argv[2],sys.argv[3],sys.argv[4])