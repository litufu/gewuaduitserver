# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AduitAdjustment
from utils import get_subject_name_by_num,get_subject_num_by_name


def aduit_ajustment(session,engine,start_time,end_time,record):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    records = json.loads(record)
    # 从数据库读取科目余额表
    aduit_adjustments = session.query(AduitAdjustment).filter((AduitAdjustment.record_time == end_time)&(AduitAdjustment.vocher_type == "审")).all()
    is_profit_and_loss_subject = False
    for i,record in enumerate(records):
        subject =record.get("subject","").split("_")
        if len(subject)==0:
            raise Exception("未录入科目")
        subject_num = subject[0]
        if subject_num.startswith("6"):
            is_profit_and_loss_subject = True
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
    #     如果是损益类科目，自动结转本年利润和利润分配
    if is_profit_and_loss_subject:
        # 删除已经存在的会计分录
        carry_forwords = session.query(AduitAdjustment).filter((AduitAdjustment.record_time == end_time)&(AduitAdjustment.vocher_type == "转"))
        for carry_forword  in carry_forwords:
            session.delete(carry_forword)
        session.commit()
        df_km = pd.read_sql_table('subjectbalance', engine)
        df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]
        df_adjustment = pd.read_sql_table('aduitadjustment', engine)
        df_adjustment_profit = df_adjustment[(df_adjustment['record_time'] == end_time) & (df_adjustment['subject_num'].str.startswith("6"))]

        df_adjustment_profit_this_year = df_adjustment_profit[~df_adjustment_profit["subject_name"].str.contains("以前年度损益调整")]
        if len(df_adjustment_profit_this_year)>0:
            # 1、结转本年损益至本年利润
            df_adjustment_profit_this_year_pivot = df_adjustment_profit_this_year.pivot_table(values=['debit', 'credit'],
                                                                                              index='subject_num',
                                                                                              aggfunc='sum')
            this_year_profit = df_adjustment_profit_this_year_pivot.debit.sum() - df_adjustment_profit_this_year_pivot.credit.sum()
            for i,subject_num in enumerate(df_adjustment_profit_this_year_pivot.index):
                debit = df_adjustment_profit_this_year_pivot.at[subject_num, "debit"]
                credit = df_adjustment_profit_this_year_pivot.at[subject_num, "credit"]
                aduit_adjustment = AduitAdjustment(
                    year=start_time.year,
                    month=end_time.month,
                    record_time=end_time,
                    vocher_type="转",
                    vocher_num=1,
                    subentry_num=i + 1,
                    description="结转本年利润",
                    subject_num=subject_num,
                    subject_name=get_subject_name_by_num(subject_num,df_km),
                    currency_type="",
                    debit=credit,
                    credit=debit,
                    debit_foreign_currency=0.00,
                    credit_foreign_currency=0.00,
                    debit_number=0.00,
                    credit_number=0.00,
                    debit_price=0.00,
                    credit_price=0.00,
                    auxiliary=""
                )
                session.add(aduit_adjustment)
            this_year_profit_adjustment = AduitAdjustment(
                year=start_time.year,
                month=end_time.month,
                record_time=end_time,
                vocher_type="转",
                vocher_num=1,
                subentry_num=len(df_adjustment_profit_this_year_pivot) + 1,
                description="结转本年利润",
                subject_num=get_subject_num_by_name("本年利润",df_km),
                subject_name="本年利润",
                currency_type="",
                debit=this_year_profit,
                credit=0.00,
                debit_foreign_currency=0.00,
                credit_foreign_currency=0.00,
                debit_number=0.00,
                credit_number=0.00,
                debit_price=0.00,
                credit_price=0.00,
                auxiliary=""
            )
            session.add(this_year_profit_adjustment)
            session.commit()
        #    2、结转本年利润至未分配利润
            this_year_profit_to_undistributed_profit  = AduitAdjustment(
                year=start_time.year,
                month=end_time.month,
                record_time=end_time,
                vocher_type="转",
                vocher_num=2,
                subentry_num=1,
                description="本年利润结转未分配利润",
                subject_num=get_subject_num_by_name("本年利润", df_km),
                subject_name="本年利润",
                currency_type="",
                debit=0.00,
                credit=this_year_profit,
                debit_foreign_currency=0.00,
                credit_foreign_currency=0.00,
                debit_number=0.00,
                credit_number=0.00,
                debit_price=0.00,
                credit_price=0.00,
                auxiliary=""
            )
            session.add(this_year_profit_to_undistributed_profit)
            undistributed_profit_this_year_profit = AduitAdjustment(
                year=start_time.year,
                month=end_time.month,
                record_time=end_time,
                vocher_type="转",
                vocher_num=2,
                subentry_num=2,
                description="本年利润结转未分配利润",
                subject_num=get_subject_num_by_name("未分配利润", df_km),
                subject_name="未分配利润",
                currency_type="",
                debit=this_year_profit,
                credit=0.00,
                debit_foreign_currency=0.00,
                credit_foreign_currency=0.00,
                debit_number=0.00,
                credit_number=0.00,
                debit_price=0.00,
                credit_price=0.00,
                auxiliary=""
            )
            session.add(undistributed_profit_this_year_profit)
            session.commit()
        # 3、结转以前年度损益至未分配利润
        df_adjustment_profit_previous_year = df_adjustment_profit[
            df_adjustment_profit["subject_name"].str.contains("以前年度损益调整")]
        if len(df_adjustment_profit_previous_year)>0:
            df_adjustment_profit_previous_year_pivot = df_adjustment_profit_previous_year.pivot_table(values=['debit', 'credit'], index='subject_num', aggfunc='sum')
            previous_year_profit = df_adjustment_profit_previous_year_pivot.debit.sum() - df_adjustment_profit_previous_year_pivot.credit.sum()
            previous_year_profit_to_undistributed_profit = AduitAdjustment(
                year=start_time.year,
                month=end_time.month,
                record_time=end_time,
                vocher_type="转",
                vocher_num=3,
                subentry_num=1,
                description="以前年度损益结转未分配利润",
                subject_num=get_subject_num_by_name("以前年度损益调整", df_km),
                subject_name="以前年度损益调整",
                currency_type="",
                debit=0.00,
                credit=previous_year_profit,
                debit_foreign_currency=0.00,
                credit_foreign_currency=0.00,
                debit_number=0.00,
                credit_number=0.00,
                debit_price=0.00,
                credit_price=0.00,
                auxiliary=""
            )
            session.add(previous_year_profit_to_undistributed_profit)
            undistributed_profit_previous_year_profit = AduitAdjustment(
                year=start_time.year,
                month=end_time.month,
                record_time=end_time,
                vocher_type="转",
                vocher_num=3,
                subentry_num=2,
                description="以前年度损益结转未分配利润",
                subject_num=get_subject_num_by_name("未分配利润", df_km),
                subject_name="未分配利润",
                currency_type="",
                debit=previous_year_profit,
                credit=0.00,
                debit_foreign_currency=0.00,
                credit_foreign_currency=0.00,
                debit_number=0.00,
                credit_number=0.00,
                debit_price=0.00,
                credit_price=0.00,
                auxiliary=""
            )
            session.add(undistributed_profit_previous_year_profit)
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

    # aduit_ajustment(session,engine,start_time,end_time,record)
    aduit_ajustment(session,engine,sys.argv[2],sys.argv[3],sys.argv[4])