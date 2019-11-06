# -*- coding:utf-8 -*-
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')
import sys
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,SubjectBalance,AccountAge,AgeSetting,ChronologicalAccount,AduitAdjustment
from utils import gen_df_line,DateEncoder,parse_auxiliary
from get_tb import recaculate_km

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


def get_subject_detail(df_subject_balance,df_auxiliary,subjects):
    '''

    :param df_subject_balance:
    :param df_auxiliary:
    :param subjects:
    :return:
    '''
    df_first_subject_balance = df_subject_balance[df_subject_balance["subject_gradation"] == 1]
    # 获取一级会计科目长度
    first_subject_num_length = len(df_first_subject_balance["subject_num"].values[0])
    # 为科目余额表添加一级科目
    df_subject_balance["first_subject_num"] = df_subject_balance["subject_num"].apply(lambda x: x[0:first_subject_num_length])


    df_subject = df_first_subject_balance[df_first_subject_balance["subject_name"].isin(subjects)]
    subject_nums = df_subject["subject_num"].values
    if len(subject_nums) > 0:
        df_subject_balance_new = df_subject_balance[(df_subject_balance["is_specific"]==True)&(df_subject_balance["first_subject_num"].isin(subject_nums))]
        df_auxiliary_new = df_auxiliary[df_auxiliary["subject_num"].isin(df_subject_balance_new["subject_num"])]
        df_subject_balance_new = df_subject_balance_new[~df_subject_balance_new["subject_num"].isin(df_auxiliary_new["subject_num"])]
        df_subject_balance_new = df_subject_balance_new[["subject_num","subject_name","direction","initial_amount","origin_debit","origin_credit","origin_terminal","debit_amount","credit_amount","terminal_amount"]]
        df_subject_balance_new["source"] = "kemu"
        df_auxiliary_new = df_auxiliary_new[["subject_num","name","direction","initial_amount","origin_debit","origin_credit","origin_terminal","debit_amount","credit_amount","terminal_amount"]]
        df_auxiliary_new = df_auxiliary_new.rename(columns={"name": "subject_name"})
        df_auxiliary_new["source"] = "hesuan"
        df_subject_detail = df_subject_balance_new.append(df_auxiliary_new, ignore_index=True)
        df_subject_detail["terminal_value"] = df_subject_detail["direction"].apply(lambda x:1 if x=="借" else -1) * df_subject_detail["terminal_amount"]
        df_subject_detail["origin_terminal_value"] = df_subject_detail["direction"].apply(lambda x:1 if x=="借" else -1) * df_subject_detail["origin_terminal"]
        df_subject_detail["search_name"] = df_subject_detail['subject_name'].str.replace(r'[\(\)]+', '')
        return df_subject_detail
    else:
        return  pd.DataFrame()

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

    df_xsz = df_xsz.copy()
    terminal_value = obj["terminal_value"]
    abs_terminal_value = abs(terminal_value)
    search_name = obj["search_name"]
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
            df_obj_xsz = df_xsz[(df_xsz["subject_num"] == subject_num) & (df_xsz["search_auxiliary"].str.contains(search_name)) & (df_xsz["debit"].abs()>0.0) ]
            occurs = get_occours(df_obj_xsz, abs_terminal_value, "debit")
            return occurs
        else:
            df_obj_xsz = df_xsz[
                (df_xsz["subject_num"] == subject_num) &
                (df_xsz["search_auxiliary"].str.contains(search_name)) &
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


def get_auxiliary_name(auxiliary_str):
    '''
    获取核算项目名称
    :param auxiliary_str:
    :return:
    '''
    res = parse_auxiliary(auxiliary_str)
    name = ""
    if "部门" in res:
        res.pop("部门")
    if len(res) == 0:
        pass
    elif len(res) == 1:
        name = list(res.values())[0]
    else:
        if "客户" in res:
            name = res["客户"]
        elif "供应商" in res:
            name = res["供应商"]
        else:
            name = list(res.values())[0]
    return name.strip()

def recaculate_auxiliary(df_auxiliary,df_xsz):
    '''
    重新计算辅助核算明细表
    :param df_auxiliary:
    :param df_xsz:
    :return:
    '''
    df_auxiliary_new = df_auxiliary[
        ["id", "start_time", "end_time", "subject_num", "subject_name","type_num","type_name",
         "code","name", "direction",  "initial_amount"
         ]
    ].copy()
    df_auxiliary_new["origin_debit"] = df_auxiliary["debit_amount"]
    df_auxiliary_new["origin_credit"] = df_auxiliary["credit_amount"]
    df_auxiliary_new["origin_terminal"] = df_auxiliary["terminal_amount"]
    df_auxiliary_new['debit_amount'] = 0.00
    df_auxiliary_new['credit_amount'] = 0.00
    df_auxiliary_new['terminal_amount'] = 0.00
    df_auxiliary_new = df_auxiliary_new.set_index(['subject_num',"name"])
    # 计算序时账发生额
    df_xsz["name"] = df_xsz["auxiliary"].apply(get_auxiliary_name)
    df_xsz_pivot = df_xsz.pivot_table(values=['debit', 'credit'], index=['subject_num',"name"], aggfunc='sum')
    for i in range(len(df_auxiliary_new)):
        subject_num_and_name = df_auxiliary_new.index[i]
        # 序时账透视表中筛选出所有科目和子科目
        try:
            df_xsz_pivot_tmp = df_xsz_pivot.loc[subject_num_and_name]
        except Exception as e:
            continue
        # 序时账借方合计
        debit = df_xsz_pivot_tmp['debit'].sum()
        # 序时账贷方合计
        credit = df_xsz_pivot_tmp['credit'].sum()
        df_auxiliary_new.at[subject_num_and_name, "debit_amount"] = debit
        df_auxiliary_new.at[subject_num_and_name, "credit_amount"] = credit
        if df_auxiliary_new.at[subject_num_and_name, "direction"] == "借":
            df_auxiliary_new.at[subject_num_and_name, "terminal_amount"] = df_auxiliary_new.at[
                                                                               subject_num_and_name, "initial_amount"] + debit - credit
        elif df_auxiliary_new.at[subject_num_and_name, "direction"] == "贷":
            df_auxiliary_new.at[subject_num_and_name, "terminal_amount"] = df_auxiliary_new.at[
                                                                               subject_num_and_name, "initial_amount"] - debit + credit
    df_auxiliary_new = df_auxiliary_new.reset_index()
    return df_auxiliary_new

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
    # 获取调整分录
    df_adjustment = pd.read_sql(session.query(AduitAdjustment).filter(AduitAdjustment.year<=end_time.year,AduitAdjustment.month<=end_time.month).statement, engine)
    # 获取以前年度所有的序时账，合并审计调整分录
    df_xsz_all = pd.read_sql(session.query(ChronologicalAccount).filter(ChronologicalAccount.year<=end_time.year,ChronologicalAccount.month<=end_time.month).statement, engine)
    df_xsz_all = df_xsz_all.append(df_adjustment)
    df_xsz_all = df_xsz_all.sort_values(by=['record_time', 'vocher_num'], ascending=False)
    df_xsz_all["search_auxiliary"] = df_xsz_all["auxiliary"].str.replace(r'[\(\)]+', '')
    # 获取当年度的序时账，合并审计调整分录
    df_xsz = pd.read_sql(session.query(ChronologicalAccount).filter(ChronologicalAccount.year==end_time.year,ChronologicalAccount.month<=end_time.month).statement, engine)
    df_xsz = df_xsz.append(df_adjustment)
    df_xsz = df_xsz.sort_values(by=['record_time','vocher_num'], ascending=False)
    df_xsz["search_auxiliary"] = df_xsz["auxiliary"].str.replace(r'[\(\)]+', '')
    # 获取科目余额表，并根据序时账重新计算科目余额表
    df_subject_balance = pd.read_sql(session.query(SubjectBalance).filter(SubjectBalance.start_time == start_time,
                                                                          SubjectBalance.end_time == end_time,
                                                                          ).statement, engine)
    df_subject_balance_new = recaculate_km(df_subject_balance,df_xsz,"audited")

    # 获取辅助核算明细表，并根据序时账重算辅助核算明细表
    df_auxiliary = pd.read_sql(session.query(Auxiliary).filter(Auxiliary.start_time == start_time,
                                                               Auxiliary.end_time == end_time,
                                                               ).statement, engine)
    # 部门辅助核算不包含
    df_auxiliary = df_auxiliary[~df_auxiliary["type_name"].str.contains("部门")]
    df_auxiliary_new = recaculate_auxiliary(df_auxiliary,df_xsz)


    for setting in settings:
        df_detail = get_subject_detail(df_subject_balance_new,df_auxiliary_new,setting["values"])
        df_detail["origin_subject"] = setting["name"]
        # 获取所有项目的发生时间
        for obj in gen_df_line(df_detail):
            occur_times = get_occour_times(obj, df_xsz_all)
            account_age = AccountAge(
                start_time= start_time,
                end_time = end_time,
                subject_num=obj["subject_num"],
                origin_subject=obj["origin_subject"],
                subject_name=obj["subject_name"],
                source=obj["source"],
                direction=obj["direction"],
                initial_amount=obj["initial_amount"],
                origin_debit = obj["origin_debit"],
                origin_credit = obj["origin_credit"],
                origin_terminal = obj["origin_terminal"],
                origin_terminal_value = obj["origin_terminal_value"],
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
    # db_path = "D:\gewuaduit\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # start_time = "2015-1-1"
    # end_time = "2015-12-31"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    save_account_occur_times_to_db(engine,session,start_time,end_time)
    sys.stdout.write("success")

