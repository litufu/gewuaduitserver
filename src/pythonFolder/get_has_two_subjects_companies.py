# -*- coding:utf-8 -*-

import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,SubjectBalance

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
        df_subject_balance_new = df_subject_balance_new[["subject_num","subject_name","direction","initial_amount","debit_amount","credit_amount","terminal_amount"]]
        df_auxiliary_new = df_auxiliary_new[["subject_num","name","direction","initial_amount","debit_amount","credit_amount","terminal_amount"]]
        df_auxiliary_new = df_auxiliary_new.rename(columns={"name": "subject_name"})
        df_subject_detail = df_subject_balance_new.append(df_auxiliary_new, ignore_index=True)
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



def get_has_two_subjects_companies(session,start_time,end_time):
    '''
    获取在应收账款、预收账款或应付账款或预付账款同时挂账的往来单位名称
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    df_accounts_receivable = get_subject_detail(session,start_time,end_time,accounts_receivable)
    df_advance_account_receivable = get_subject_detail(session,start_time,end_time,advance_account_receivable)
    df_advance_payment = get_subject_detail(session,start_time,end_time,advance_payment)
    df_accounts_payable = get_subject_detail(session,start_time,end_time,accounts_payable)
    df_contractual_assets = get_subject_detail(session,start_time,end_time,contractual_assets)
    df_contractual_liability = get_subject_detail(session,start_time,end_time,contractual_liability)

    receivable_names = get_df_intersection(df_accounts_receivable,df_advance_account_receivable)
    payable_names = get_df_intersection(df_advance_payment,df_accounts_payable)
    contractual_names = get_df_intersection(df_contractual_assets,df_contractual_liability)
    res = {"receivable":receivable_names,"payable":payable_names,"contractual":contractual_names}
    sys.stdout.write(json.dumps(res))



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
    get_has_two_subjects_companies(session,start_time,end_time)