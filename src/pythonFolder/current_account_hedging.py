import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,SubjectBalance,AduitAdjustment
from add_aduit_adjustment import aduit_ajustment

accounts_receivable = ["应收账款","应收帐款"]
advance_account_receivable = ["预收账款","预收款项","预收帐款"]
contractual_assets = ["合同资产"]
contractual_liability = ["合同负债"]
advance_payment = ["预付账款","预付款项"]
accounts_payable = ["应付账款","应付帐款"]


def get_subject_detail(session,start_time,end_time,subjects):
    '''
    获取莫客户的明细表
    :param session:
    :param start_time:
    :param end_time:
    :param subjects: ["应收账款","应收帐款"]
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df_subject_balance = pd.read_sql(session.query(SubjectBalance).filter(SubjectBalance.start_time == start_time,
                                                                          SubjectBalance.end_time == end_time,
                                                                          ).statement, engine)
    df_first_subject_balance = df_subject_balance[df_subject_balance["subject_gradation"] == 1]
    # 获取一级会计科目长度
    first_subject_num_length = len(df_first_subject_balance["subject_num"].values[0])
    # 为科目余额表添加一级科目
    df_subject_balance["first_subject_num"] = df_subject_balance["subject_num"].apply(lambda x: x[0:first_subject_num_length])
    df_auxiliary = pd.read_sql(session.query(Auxiliary).filter(Auxiliary.start_time == start_time,
                                                               Auxiliary.end_time == end_time,
                                                               ).statement, engine)
    # 部门辅助核算不包含
    df_auxiliary = df_auxiliary[~df_auxiliary["type_name"].str.contains("部门")]
    df_subject = df_first_subject_balance[df_first_subject_balance["subject_name"].isin(subjects)]
    subject_nums = df_subject["subject_num"].values
    if len(subject_nums) > 0:
        df_subject_balance_new = df_subject_balance[(df_subject_balance["is_specific"]==True)&(df_subject_balance["first_subject_num"].isin(subject_nums))]
        df_auxiliary_new = df_auxiliary[df_auxiliary["subject_num"].isin(df_subject_balance_new["subject_num"])]
        df_subject_balance_new = df_subject_balance_new[~df_subject_balance_new["subject_num"].isin(df_auxiliary_new["subject_num"])]
        df_subject_balance_new = df_subject_balance_new.copy()
        df_auxiliary_new = df_auxiliary_new.copy()
        df_subject_balance_new["name"] = df_subject_balance_new["subject_name"]
        df_subject_balance_new["source"] = "kemu"
        df_auxiliary_new["source"] = "hesuan"
        df_subject_detail = df_subject_balance_new.append(df_auxiliary_new, ignore_index=True,sort=False)
        df_subject_detail["terminal_value"] = df_subject_detail["direction"].apply(lambda x: 1 if x == "借" else -1) * \
                                              df_subject_detail["terminal_amount"]
        return df_subject_detail
    else:
        return  pd.DataFrame()


def get_df_intersection(df1,df2):
    if len(df1)== 0 or len(df2) == 0:
        return []
    else:
        df1_names = set(df1["name"].to_list())
        df2_names = set(df2["name"].to_list())
        intersection_names = list(df1_names.intersection(df2_names))
        return intersection_names


def get_adjustment(session, engine, start_time, end_time,df_asset,df_liability):
    names = get_df_intersection(df_asset, df_liability)
    for name in names:
        df_asset_subject = df_asset[df_asset["name"]==name]
        df_liability_subject = df_liability[df_liability["name"]==name]
        asset_value = df_asset_subject["terminal_value"].sum()
        liability_value = df_liability_subject["terminal_value"].sum()
        adjust_value = abs(asset_value) if abs(liability_value)>abs(asset_value) else abs(liability_value)
        if adjust_value >0.0:
            if ( asset_value>0 and liability_value >0 ) or ( asset_value<0 and  liability_value<0 ):
                pass
            else:
                asset_subject_num = df_asset_subject["subject_num"].values[0]
                liability_subject_num = df_liability_subject["subject_num"].values[0]
                asset_subject_name = df_asset_subject["subject_name"].values[0]
                liability_subject_name = df_liability_subject["subject_name"].values[0]
                assert_source = df_asset_subject["source"].values[0]
                liability_source = df_liability_subject["source"].values[0]
                if assert_source == "hesuan":
                    assert_type_name = df_asset_subject["type_name"].values[0]
                    assert_name = df_asset_subject["name"].values[0]
                    assert_auxiliary = "{}_{}".format(assert_type_name, assert_name)
                else:
                    assert_auxiliary = ""
                if liability_source == "hesuan":
                    liability_type_name = df_liability_subject["type_name"].values[0]
                    liability_name = df_liability_subject["name"].values[0]
                    liability_auxiliary = "{}_{}".format(liability_type_name, liability_name)
                else:
                    liability_auxiliary = ""
                adjustments = [
                    {
                    "description": "往来对冲",
                    "record_time": end_time,
                    "subject": "{}_{}".format(asset_subject_num, asset_subject_name),
                    "currency_type": "RMB",
                    "foreign_currency": 0.00,
                    "debit": 0.00,
                    "credit": adjust_value,
                    "auxiliary": assert_auxiliary
                    },
                    {
                        "description": "往来对冲",
                        "record_time": end_time,
                        "subject": "{}_{}".format(liability_subject_num, liability_subject_name),
                        "currency_type": "RMB",
                        "foreign_currency": 0.00,
                        "debit": adjust_value,
                        "credit": 0.00,
                        "auxiliary": liability_auxiliary
                    },
                ]
                record = json.dumps(adjustments)
                aduit_ajustment(session, engine, start_time, end_time, record, vocher_type="冲")


def deleteHedgingEntries(session,start_time,end_time):
    '''
    删除本期对冲凭证
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    objs = session.query(AduitAdjustment).filter(AduitAdjustment.year == start_time.year, AduitAdjustment.month == end_time.month,AduitAdjustment.vocher_type=="冲").all()
    for obj in objs:
        session.delete(obj)
    session.commit()


def current_account_hedging(session,start_time,end_time):
    '''
    获取在应收账款、预收账款或应付账款或预付账款同时挂账的往来单位名称
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    deleteHedgingEntries(session,start_time,end_time)
    df_accounts_receivable = get_subject_detail(session,start_time,end_time,accounts_receivable)
    df_advance_account_receivable = get_subject_detail(session,start_time,end_time,advance_account_receivable)
    get_adjustment(session, engine, start_time, end_time, df_accounts_receivable, df_advance_account_receivable)

    df_advance_payment = get_subject_detail(session,start_time,end_time,advance_payment)
    df_accounts_payable = get_subject_detail(session,start_time,end_time,accounts_payable)
    get_adjustment(session, engine, start_time, end_time, df_advance_payment, df_accounts_payable)

    df_contractual_assets = get_subject_detail(session,start_time,end_time,contractual_assets)
    df_contractual_liability = get_subject_detail(session,start_time,end_time,contractual_liability)
    get_adjustment(session, engine, start_time, end_time, df_contractual_assets, df_contractual_liability)

    sys.stdout.write("success")



if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    current_account_hedging(session,start_time,end_time)