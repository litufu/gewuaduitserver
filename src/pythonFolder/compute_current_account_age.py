# -*- coding:utf-8 -*-
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')
import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,SubjectBalance,AccountAge,AgeSetting
from utils import gen_df_line,DateEncoder

accounts_receivable = ["应收账款","应收帐款"]
advance_account_receivable = ["预收账款","预收款项","预收帐款"]
contractual_assets = ["合同资产"]
contractual_liability = ["合同负债"]
advance_payment = ["预付账款","预付款项"]
accounts_payable = ["应付账款","应付帐款"]
other_accounts_receivable = ["其他应收款"]
other_accounts_payable = ["其他应付款"]
settings = [
    {"name":"应收账款","values":accounts_receivable},
    {"name":"预收款项","values":advance_account_receivable},
    {"name":"预付款项","values":advance_payment},
    {"name":"应付账款","values":accounts_payable},
    {"name":"合同资产","values":contractual_assets},
    {"name":"合同负债","values":contractual_liability},
    {"name":"其他应收款","values":other_accounts_receivable},
    {"name":"其他应付款","values":other_accounts_payable},
]

def get_subject_detail(session,start_time,end_time,subjects):
    '''
    获取莫客户的明细表
    :param session:
    :param start_time:
    :param end_time:
    :param subjects: ["应收账款","应收帐款"]
    :return:
    '''

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
        df_subject_balance_new = df_subject_balance_new[["subject_num","subject_name","direction","initial_amount","debit_amount","credit_amount","terminal_amount"]]
        df_subject_balance_new["source"] = "kemu"
        df_auxiliary_new = df_auxiliary_new[["subject_num","name","direction","initial_amount","debit_amount","credit_amount","terminal_amount"]]
        df_auxiliary_new = df_auxiliary_new.rename(columns={"name": "subject_name"})
        df_auxiliary_new["source"] = "hesuan"
        df_subject_detail = df_subject_balance_new.append(df_auxiliary_new, ignore_index=True)
        df_subject_detail["terminal_value"] = df_subject_detail["direction"].apply(lambda x:1 if x=="借" else -1) * df_subject_detail["terminal_amount"]
        return df_subject_detail
    else:
        return  pd.DataFrame()


def get_df_intersection(df1,df2):
    if len(df1)== 0 or len(df2) == 0:
        return []
    else:
        df1_subject_names = set(df1["subject_name"].to_list())
        df2_subject_names = set(df2["subject_name"].to_list())
        intersection_names = list(df1_subject_names.intersection(df2_subject_names))
        return intersection_names

def get_occours(df_obj_xsz,abs_terminal_value,direction):
    sum = 0.0
    occurs = []
    for item in gen_df_line(df_obj_xsz):
        sum = sum + item.get(direction)
        if sum <= abs_terminal_value:
            occurs.append({"occur_time": item["record_time"], "value": item.get(direction)})
        else:
            occurs.append(
                {"occur_time": item["record_time"], "value": abs_terminal_value - (sum - item.get(direction))})
            break
    if sum < abs_terminal_value:
        occurs.append(
            {"occur_time": 633801600000 , "value": abs_terminal_value - sum })
    return occurs

def get_occour_times(obj,df_xsz):
    # 对序时账按照记账时间降序排列

    terminal_value = obj["terminal_value"]
    abs_terminal_value = abs(terminal_value)
    subject_name = obj["subject_name"]
    subject_num = obj["subject_num"]

    if obj["source"] == "kemu":
        if terminal_value > 0:
            df_obj_xsz = df_xsz[(df_xsz["subject_num"] == subject_num)&(df_xsz["debit"].abs()>0.0)]
            occurs = get_occours(df_obj_xsz, abs_terminal_value, "debit")
            return occurs

        else:
            df_obj_xsz = df_xsz[(df_xsz["subject_num"] == subject_num) & (df_xsz["credit"].abs() > 0.0)]
            occurs = get_occours(df_obj_xsz, abs_terminal_value, "credit")
            return occurs
    elif obj["source"] == "hesuan":
        if terminal_value > 0.0:
            df_obj_xsz = df_xsz[(df_xsz["subject_num"] == subject_num) & (df_xsz["auxiliary"].str.contains(subject_name)) & (df_xsz["debit"].abs()>0.0) ]
            occurs = get_occours(df_obj_xsz, abs_terminal_value, "debit")
            return occurs
        else:
            df_obj_xsz = df_xsz[
                (df_xsz["subject_num"] == subject_num) &
                (df_xsz["auxiliary"].str.contains(subject_name)) &
                (df_xsz["credit"].abs() > 0.0)
                ]
            occurs = get_occours(df_obj_xsz, abs_terminal_value, "credit")
            return occurs
    else:
        raise Exception("明细科目来源不明")


def deleteAccountAge(session,start_time,end_time):
    '''
    删除本期已经分过的账龄
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    objs = session.query(AccountAge).filter(AccountAge.start_time ==start_time,AccountAge.end_time==end_time).all()
    for obj in objs:
        session.delete(obj)
    session.commit()

def save_account_occur_times_to_db(engine,session,start_time,end_time):
    '''
    将往来款的发生时间放在数据库
    :param engine:
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    deleteAccountAge(session, start_time, end_time)
    df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    df_xsz = df_xsz.sort_values(by=['record_time'], ascending=False)
    for setting in settings:
        df_detail = get_subject_detail(session,start_time,end_time,setting["values"])
        df_detail["origin_subject"] = setting["name"]
        # 获取所有项目的发生时间
        for obj in gen_df_line(df_detail):
            occur_times = get_occour_times(obj, df_xsz)
            account_age = AccountAge(
                start_time= start_time,
                end_time = end_time,
                subject_num=obj["subject_num"],
                origin_subject=obj["origin_subject"],
                subject_name=obj["subject_name"],
                source=obj["source"],
                direction=obj["direction"],
                initial_amount=obj["initial_amount"],
                debit_amount=obj["debit_amount"],
                credit_amount=obj["credit_amount"],
                terminal_amount=obj["terminal_amount"],
                terminal_value=obj["terminal_value"],
                occour_times = json.dumps(occur_times,cls=DateEncoder)
            )
            session.add(account_age)
        session.commit()



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
    save_account_occur_times_to_db(engine,session,start_time,end_time)
    sys.stdout.write("success")

