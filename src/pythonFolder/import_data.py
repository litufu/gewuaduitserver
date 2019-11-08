# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import math
from database import Auxiliary, SubjectBalance, ChronologicalAccount
from utils import str_to_float,check_start_end_date



def save_km(start_time, end_time, km_path,session):
    '''
    科目编号	科目名称	科目类别	借贷方向	是否明细科目	科目级次
    账面期初数	账面借方发生额	账面贷方发生额	账面期末数
    :param start_time:科目余额表开始时间，如20019-1-1
    :param end_time:科目余额表结束时间，如20019-12-31
    :return:
    '''
    # 读取文件
    df = pd.read_excel(km_path, index_col=0)
    columns = [column for column in df]
    names = ["科目编号","科目名称","科目类别","借贷方向","是否明细科目","科目级次","账面期初数","账面借方发生额","账面贷方发生额","账面期末数"]
    columns_right = [False for name in names if name not in columns]
    if False in columns_right:
        raise Exception("项目名称必须包含科目编号,科目名称,科目类别,借贷方向,是否明细科目,科目级次,账面期初数,账面借方发生额,账面贷方发生额,账面期末数等信息")

    # 转换起止时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)
    # 检查是否已经存储科目余额表
    kms = session.query(SubjectBalance).filter(
                                               SubjectBalance.start_time == start_time,
                                               SubjectBalance.end_time == end_time).all()
    #如果已经存储了，则替代原来的
    if len(kms) > 0:
        for km in kms:
            session.delete(km)
        session.commit()

    # 重新索引
    df = df.rename(index=str, columns={
        "科目编号": "subject_num",
        "科目名称": "subject_name",
        "科目类别": "subject_type",
        "借贷方向": "direction",
        "是否明细科目": "is_specific",
        "科目级次": "subject_gradation",
        "账面期初数": "initial_amount",
        "账面借方发生额": "debit_amount",
        "账面贷方发生额": "credit_amount",
        "账面期末数": "terminal_amount",
    })
    df = df[['subject_num', 'subject_name', 'subject_type', 'direction',
             'is_specific', 'subject_gradation', 'initial_amount', 'debit_amount',
             'credit_amount', 'terminal_amount'
             ]]
    # 存入数据库
    for i in range(len(df)):
        subject_num = str(df.iat[i, 0])
        subject_name = df.iat[i, 1]
        subject_type = df.iat[i, 2]
        direction = df.iat[i, 3]
        is_specific = df.iat[i, 4] == "是"
        subject_gradation = str(df.iat[i, 5])
        initial_amount = str_to_float(df.iat[i, 6])
        debit_amount = str_to_float(df.iat[i, 7])
        credit_amount = str_to_float(df.iat[i, 8])
        terminal_amount = str_to_float(df.iat[i, 9])
        # 判断科目余额表是否正确
        if direction == "借":
            value = abs(Decimal(initial_amount) +Decimal(debit_amount)  - Decimal(credit_amount) - Decimal(terminal_amount))
            if value > 0.000001:
                raise Exception("{}的期初{}+本期借方{}-本期贷方{}不等于期末数{}".format(subject_name,initial_amount,debit_amount,credit_amount,terminal_amount))
        else:
            value = abs(
                Decimal(initial_amount) - Decimal(debit_amount) + Decimal(credit_amount) - Decimal(terminal_amount))
            if  value > 0.000001:
                raise Exception("{}的期初{}-本期借方{}+本期贷方{}不等于期末数{}".format(subject_name,initial_amount,debit_amount,credit_amount,terminal_amount))

        km = SubjectBalance(start_time=start_time,
                            end_time=end_time,
                            subject_num=subject_num, subject_name=subject_name, subject_type=subject_type,
                            direction=direction, is_specific=is_specific, subject_gradation=int(subject_gradation),
                            initial_amount=initial_amount, debit_amount=debit_amount, credit_amount=credit_amount,
                            terminal_amount=terminal_amount
                            )
        session.add(km)
    session.commit()


def save_xsz(start_time, end_time, xsz_path,session):
    '''
    会计年	会计月	记账时间	凭证编号	凭证种类	编号	业务说明
    	科目编号	科目名称	借方发生额	贷方发生额	借方发生额_外币	贷方发生额_外币	借方数量	贷方数量	借方单价	贷方单价
    			货币种类		核算项目名称

    :param xsz_path:
    :return:
    '''
    # 转换起止时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)

    # 读取序时账
    df = pd.read_excel(xsz_path, index_col=0)
    # 检查序时账是否符合规范
    columns = [column for column in df]
    names = ["会计年", "会计月", "记账时间", "凭证编号", "凭证种类", "编号", "业务说明", "科目编号", "科目名称",
             "借方发生额","贷方发生额","借方发生额_外币","贷方发生额_外币","借方数量","贷方数量","借方单价","贷方单价",
             "货币种类","核算项目名称"
             ]
    columns_right = [False for name in names if name not in columns]
    if False in columns_right:
        raise Exception("项目名称不符合序时账导入规则")
    # 重新索引
    df = df.rename(index=str, columns={
        "会计年": "year",
        "会计月": "month",
        "记账时间": "record_time",
        "凭证编号": "vocher_num",
        "凭证种类": "vocher_type",
        "编号": "subentry_num",
        "业务说明": "description",
        "科目编号": "subject_num",
        "科目名称": "subject_name",
        "借方发生额": "debit",
        "贷方发生额": "credit",
        "借方发生额_外币": "debit_foreign_currency",
        "贷方发生额_外币": "credit_foreign_currency",
        "借方数量": "debit_number",
        "贷方数量": "credit_number",
        "借方单价": "debit_price",
        "贷方单价": "credit_price",
        "货币种类": "currency_type",
        "核算项目名称": "auxiliary",
    })
    df = df[['year', 'month', 'record_time', 'vocher_num', 'vocher_type', 'subentry_num', 'description', 'subject_num',
             'subject_name', 'debit', 'credit', 'debit_foreign_currency', 'credit_foreign_currency', 'debit_number',
             'credit_number', 'debit_price', 'credit_price', 'currency_type', 'auxiliary'
             ]]

    # 检查是否已经存储序时账,存储则删除
    min_month = int(df.loc[:,'month'].min())
    print(min_month)
    max_month = int(df.loc[:,'month'].max())
    print(max_month)
    min_year = int(df.loc[:,'year'].min())
    print(min_year)
    max_year = int(df.loc[:,'year'].max())
    print(max_year)
    if ( min_year!= start_time.year) or (max_year != end_time.year) or  (max_month != end_time.month) :
        raise Exception("序时账实际期间与上传的数据期间不一致")

    xszs = session.query(ChronologicalAccount).filter(ChronologicalAccount.year == start_time.year,ChronologicalAccount.month>=min_month,ChronologicalAccount.month<=max_month).all()
    if len(xszs) > 0:
        for xsz in xszs:
            session.delete(xsz)
        session.commit()

    #     检查借贷方是否相等
    if not math.isclose(df['debit'].map(lambda x: str_to_float(x)).sum(), df['credit'].map(lambda x: str_to_float(x)).sum(), rel_tol=1e-5):
        raise Exception("{}序时账借方发生额和贷方发生额合计不一致")
    #     存储到数据库
    for i in range(len(df)):
        year = str(df.iat[i, 0])
        month = str(df.iat[i, 1])
        record_time = str(df.iat[i, 2])
        record_time = datetime.strptime(record_time, '%Y%m%d')
        vocher_num = int(df.iat[i, 3])
        vocher_type = str(df.iat[i, 4])
        subentry_num = int(df.iat[i, 5])
        description = df.iat[i, 6]
        subject_num = str(df.iat[i, 7])
        subject_name = df.iat[i, 8]
        debit = str_to_float(df.iat[i, 9])
        credit = str_to_float(df.iat[i, 10])
        debit_foreign_currency = str_to_float(df.iat[i, 11])
        debit_foreign_currency = debit_foreign_currency if debit_foreign_currency else 0.00
        credit_foreign_currency = str_to_float(df.iat[i, 12])
        credit_foreign_currency = credit_foreign_currency if credit_foreign_currency else 0.00
        debit_number = str_to_float(df.iat[i, 13])
        debit_number = debit_number if debit_number else 0.00
        credit_number = str_to_float(df.iat[i, 14])
        credit_number = credit_number if credit_number else 0.00
        debit_price = str_to_float(df.iat[i, 15])
        debit_price = debit_price if debit_price else 0.00
        credit_price = str_to_float(df.iat[i, 16])
        credit_price = credit_price if credit_price else 0.00
        currency_type = df.iat[i, 17]
        currency_type = currency_type if currency_type else "人民币"
        auxiliary = df.iat[i, 18]
        auxiliary = auxiliary if auxiliary else ""
        chronologicalaccount = ChronologicalAccount(year=int(year),
                                                    month=int(month), record_time=record_time, vocher_type=vocher_type,
                                                    vocher_num=vocher_num, subentry_num=subentry_num,
                                                    description=description, subject_num=subject_num,
                                                    subject_name=subject_name, currency_type=currency_type, debit=debit,
                                                    credit=credit, debit_foreign_currency=debit_foreign_currency,
                                                    credit_foreign_currency=credit_foreign_currency,
                                                    debit_number=debit_number,
                                                    credit_number=credit_number, debit_price=debit_price,
                                                    credit_price=credit_price,
                                                    auxiliary=auxiliary
                                                    )
        session.add(chronologicalaccount)
    session.commit()


def save_hs(start_time, end_time, hs_path,session):
    '''
    科目名称	科目编号	核算项目类型编号	核算项目类型名称	借贷方向	核算项目编号	核算项目名称
    账面期初数	账面借方发生额	账面贷方发生额 账面期末数
    期初数量	借方数量	贷方数量		期末数量

    :param hs_path:
    :return:
    '''
    # 转换起止时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)

    # 读取辅助核算表
    df = pd.read_excel(hs_path, index_col=0)
    # 检查核算表是否符合规范
    columns = [column for column in df]
    names = ["科目名称", "科目编号", "核算项目类型编号", "核算项目类型名称", "核算项目编号", "核算项目名称", "借贷方向", "账面期初数", "账面借方发生额",
             "账面贷方发生额", "账面期末数"]
    columns_right = [False for name in names if name not in columns]
    if False in columns_right:
        raise Exception("项目名称不符合辅助核算导入规则")

    df = df.rename(index=str, columns={
        "科目名称": "subject_name",
        "科目编号": "subject_num",
        "核算项目类型编号": "type_num",
        "核算项目类型名称": "type_name",
        "核算项目编号": "code",
        "核算项目名称": "name",
        "借贷方向": "direction",
        "账面期初数": "initial_amount",
        "账面借方发生额": "debit_amount",
        "账面贷方发生额": "credit_amount",
        "账面期末数": "terminal_amount",
        "期初数量": "initial_num",
        "借方数量": "debit_num",
        "贷方数量": "credit_num",
        "期末数量": "terminal_num",
    })
    # 检查是否已经存核算
    hs = session.query(Auxiliary).filter(
                                          Auxiliary.start_time == start_time,
                                          Auxiliary.end_time == end_time).all()
    # 如果已经存储了，则替代原来的
    if len(hs) > 0:
        for h in hs:
            session.delete(h)
        session.commit()
    # 开始存储
    if "initial_num" in df.columns:
        df = df[['subject_name', 'subject_num', 'type_num', 'type_name', 'code', 'name', 'direction', 'initial_amount',
                 'debit_amount', 'credit_amount', 'terminal_amount', 'initial_num', 'debit_num', 'credit_num',
                 'terminal_num'
                 ]]
        for i in range(len(df)):
            subject_name = df.iat[i, 0]
            subject_num = str(df.iat[i, 1])
            type_num = str(df.iat[i, 2])
            type_name = str(df.iat[i, 3])
            code = str(df.iat[i, 4])
            name = str(df.iat[i, 5])
            direction = str(df.iat[i, 6])
            initial_amount = str_to_float(df.iat[i, 7])
            debit_amount = str_to_float(df.iat[i, 8])
            credit_amount = str_to_float(df.iat[i, 9])
            terminal_amount = str_to_float(df.iat[i, 10])
            initial_num = str_to_float(df.iat[i, 11])
            debit_num = str_to_float(df.iat[i, 12])
            credit_num = str_to_float(df.iat[i, 13])
            terminal_num = str_to_float(df.iat[i, 14])

            if direction == "借":
                if not math.isclose(initial_amount + debit_amount - credit_amount, terminal_amount, rel_tol=1e-5):
                    raise Exception("辅助核算{}期初+本期借方-本期贷方不等于期末数".format(code))
            else:
                if not math.isclose(initial_amount - debit_amount + credit_amount, terminal_amount, rel_tol=1e-5):
                    raise Exception("辅助核算{}期初+本期借方-本期贷方不等于期末数".format(code))

            auxiliary = Auxiliary(subject_num=subject_num,
                                  start_time=start_time, end_time=end_time,
                                  subject_name=subject_name, type_name=type_name, type_num=type_num, code=code,
                                  name=name, direction=direction, initial_amount=initial_amount,
                                  debit_amount=debit_amount,
                                  credit_amount=credit_amount, terminal_amount=terminal_amount, initial_num=initial_num,
                                  debit_num=debit_num, credit_num=credit_num, terminal_num=terminal_num)
            session.add(auxiliary)
        session.commit()
    else:
        df = df[['subject_name', 'subject_num', 'type_num', 'type_name', 'code', 'name', 'direction',
                 'initial_amount','debit_amount', 'credit_amount', 'terminal_amount'
                 ]]
        for i in range(len(df)):
            subject_name = df.iat[i, 0]
            subject_num = str(df.iat[i, 1])
            type_num = str(df.iat[i, 2])
            type_name = str(df.iat[i, 3])
            code = str(df.iat[i, 4])
            name = str(df.iat[i, 5])
            direction = str(df.iat[i, 6])
            initial_amount = str_to_float(df.iat[i, 7])
            debit_amount = str_to_float(df.iat[i, 8])
            credit_amount = str_to_float(df.iat[i, 9])
            terminal_amount = str_to_float(df.iat[i, 10])
            initial_num = 0.00
            debit_num = 0.00
            credit_num = 0.00
            terminal_num = 0.00
            auxiliary = Auxiliary(subject_num=subject_num,
                                  subject_name=subject_name, type_name=type_name, type_num=type_num, code=code,
                                  name=name, direction=direction, initial_amount=initial_amount,
                                  debit_amount=debit_amount, start_time=start_time, end_time=end_time,
                                  credit_amount=credit_amount, terminal_amount=terminal_amount, initial_num=initial_num,
                                  debit_num=debit_num, credit_num=credit_num, terminal_num=terminal_num)
            session.add(auxiliary)
        session.commit()





def save_to_db(session,start_time,end_time,path,type):
    if type == "SUBJECTBALANCE":
        save_km(start_time,end_time,path,session)
    elif type =="CHRONOLOGICALACCOUNT":
        save_xsz(start_time,end_time,path,session)
    elif type == "AUXILIARYACCOUNTING":
        save_hs(start_time,end_time,path,session)
    else:
        raise Exception("上传数据类型错误")


if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\db\cjz6d8rpd0nat0720w8yj2ave-ck2ok4ozx000i07205dds201w.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    record = sys.argv[4]
    # start_time="2014-1-1"
    # end_time="2014-12-31"
    # record ='[{"fileId":"ck2ovcr7600er0720rwl2izyj","storeFilePath":"./uploads/ck2ovcr7600er0720rwl2izyj-km.xlsx","uploadType":"SUBJECTBALANCE"},{"fileId":"ck2ovcr7q00ew07200124lygg","storeFilePath":"./uploads/ck2ovcr7q00ew07200124lygg-pz.xlsx","uploadType":"CHRONOLOGICALACCOUNT"},{"fileId":"ck2ovcr8j00f10720akg43ppw","storeFilePath":"./uploads/ck2ovcr8j00f10720akg43ppw-hs.xlsx","uploadType":"AUXILIARYACCOUNTING"}]'
    records = json.loads(record)
    for record in records:
        path = record["storeFilePath"]
        type = record["uploadType"]
        save_to_db(session, start_time, end_time, path, type)
    print("success")

