import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups') # uncomment to suppress the UserWarning
import sys
import pandas as pd
import numpy as np
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,CustomerAnalysis,TransactionEvent




# 1、目的：寻找到异常的客户
# 客户付款方式：汇票、银行、现金。检查是否有异常付款方式的供应商。
# 客户付款时间：销售与收款之间的间隔。检查给予的信用期间是否发生明显的变化。
# 客户付款金额：销售金额与收款金额之间的差异。
# 向客户销售时间：根据销售金额、两次销售之间的间隔，计算每次销售后大概的每日消耗金额。检查客户是否存在大额存货的情况下依旧采购。
# 2、客户分析流程：
# 2.1从辅助核算中获取客户名录
# 2.2获取所有与客户有关的（应收、预收、合同负债）凭证
# 2.3年度销售金额
# 年度收款金额
# 年度销售次数
# 年度收款次数
# 收款方式统计表（现金、银行存款、应收票据）
#获取月度销售金额
#获取月度收款金额
#本月销售与下一次销售之间相差的月份
# 客户本月采购后每月消耗金额
# 客户月度消耗金额平均值
# 客户月耗方差和标准差
# 本月销售与下次收款之间时间差异
# 销售和下次收款时间差平均值
# 销售和下次收款时间差方差和标准层
# 本月销售金额与下次收款金额之间的差异
# 本月销售金额与下次收款金额之间的差异平均值
# 本月销售金额与下次收款金额之间的差异方差和标准层
# 3、相关字段名：
# 客户名称。本期销售金额、本期收款金额、本期销售次数、本期销售次数、本期销售方式、月度平均销售额、月度平均销售额、客户月耗平均值、客户月耗方差、收款期限平均值、收款期限方差、收款差额平均值、收款差额方差
# 4、计算公式
#本期采购金额 = 应收预收合同负债贷方发生额
#本期付款金额 = 应收预收合同负债借方发生额
# 本期销售次数 = 应收预收合同负债借方发生次数
# 本期收款次数 = 应收预收合同负债贷方发生次数
# 本期收款方式 = 应收预收合同负债贷方时，对方科目名称是银行存款、现金、应收票据等
# 月度平均销售额 = 本期销售金额/本期月数
# 月度平均收款额 = 本期收款金额 /本期月数
# 客户月耗平均值 = sum（本次销售 /本次销售与下次销售相差的月份/（销售次数-1）
# 客户月耗方差 = sum(（月耗-平均值）**2)/(销售次数-1）
# 收款期限平均值 = sum(本次销售与下次收款期间相差月份）/（收款次数-1）
# 收款期限方差 = sum(（收款期限-平均值）**2)/(收款次数-1）
# 收款差额平均值 = sum(本次销售金额与下次收款金额差额）/(收款次数-1）
# 收款差额方差 = sum(（收款差额-平均值）**2)/(收款次数-1）


def get_customers_name(session,start_time,end_time):
    '''
    2.1从辅助核算中获取客户名录
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    customers = []
    auxiliaries = session.query(Auxiliary).filter(Auxiliary.start_time==start_time,Auxiliary.end_time==end_time).all()
    for auxiliary in auxiliaries:
        if "客户" in auxiliary.type_name:
            customers.append(auxiliary.name)
    return customers


def get_transaction_events(engine,start_time,end_time):
    '''
    获取本期的凭证分析序时账
    :param engine:
    :param start_time:
    :param end_time:
    :return:
    '''
    return pd.read_sql(session.query(TransactionEvent).filter(TransactionEvent.start_time ==start_time,
                                                                             TransactionEvent.end_time==end_time,
                                                                             ).statement, engine)

def get_customer_entry(df_transactionEvent,customer_name):
    '''
    2.2根据序时账和供应商名称，筛选出所有的供应商凭证
    :param df_transactionEvent:序时账
    :param customer_name:客户名称
    :return:获取所有与客户有关的（应收、预收、合同负债）凭证
    '''
    df_customer_transactionEvent = df_transactionEvent[(df_transactionEvent["auxiliary"].str.contains(customer_name))&
                                                       (df_transactionEvent["tb_subject"].isin(["应收账款","预收款项","合同负债"]))]

    df_customer_record = df_customer_transactionEvent[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    # 获取相反凭证的完整借贷方
    df_customer_entries = pd.merge(df_transactionEvent, df_customer_record, how="inner",
                                     on=["month", "vocher_num", "vocher_type"])
    return df_customer_entries


def get_sale_amount(df_customer_entries,customer_name):
    '''
    获取本期向客户销售的金额
    :param df_customer_entries:客户凭证
    :param customer_name:客户名称
    :return:
    '''
    # 获取借方大于0的，包含客户名称的行
    df_customer_entries = df_customer_entries[
        (df_customer_entries["auxiliary"].str.contains(customer_name))&
        (df_customer_entries["debit"].abs()>0)
    ]
    return df_customer_entries["debit"].sum()

def get_sale_times(df_customer_entries,customer_name):
    '''
    获取本期从供应商购买的次数
    :param df_customer_entries:客户凭证
    :param supplier_name:客户名称
    :return:
    '''
    # 获取借方大于0的，包含客户名称的行
    df_customer_entries = df_customer_entries[
        (df_customer_entries["auxiliary"].str.contains(customer_name))&
        (df_customer_entries["debit"].abs()>0)
    ]
    return len(df_customer_entries)

def get_receivable_amount(df_customer_entries,customer_name):
    '''
    获取本期从客户收到的金额
    :param df_customer_entries:客户凭证
    :param customer_name:客户名称
    :return:
    '''
    # 获取贷方大于0的，包含供应商名称的行
    df_customer_entries = df_customer_entries[
        (df_customer_entries["auxiliary"].str.contains(customer_name))&
        (df_customer_entries["credit"].abs()>0)
    ]
    return df_customer_entries["credit"].sum()

def get_receivable_times(df_customer_entries,customer_name):
    '''
    获取本期从客户收款的次数
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:
    '''
    # 获取贷方大于0的，包含客户名称的行
    df_customer_entries = df_customer_entries[
        (df_customer_entries["auxiliary"].str.contains(customer_name))&
        (df_customer_entries["credit"].abs()>0)
    ]
    return len(df_customer_entries["credit"])

def get_receivable_method(df_customer_entries,customer_name):
    '''
    获取本期从客户收款方式
    :param df_customer_entries:客户凭证
    :param customer_name:客户名称
    :return:"银行存款、库存现金、应收票据
    '''
    methods_set = {"银行存款","库存现金","应收票据"}
    # 获取贷方大于0的，包含客户名称的行
    df_customer_entries = df_customer_entries[
        (df_customer_entries["auxiliary"].str.contains(customer_name))&
        (df_customer_entries["credit"].abs()>0)
    ]
    subjects = []
    for opposite_subjects in df_customer_entries["opposite_subjects"].to_list():
        tmp = json.loads(opposite_subjects)
        subjects.extend(tmp)
    subjects_set = set(subjects)
    methods = list(methods_set.intersection(subjects_set))
    methods.sort()
    method = "、".join(methods)
    return method

def get_consumption_per_month(months,df_customer_entries,customer_name,sale_times,sale_amount):
    '''
    获取客户每月消耗平均数和方差
    :param months:本期月份数
    :param df_customer_entries:客户凭证
    :param customer_name:客户名称
    :param sale_times:销售次数
    :param sale_amount:销售金额
    :return:
    '''


    if sale_times >= 2:
        df_customer_entries = df_customer_entries[
            (df_customer_entries["auxiliary"].str.contains(customer_name)) &
            (df_customer_entries["debit"].abs() > 0)
        ]
        df_customer_purchase = pd.pivot_table(df_customer_entries, values="debit", index="month",aggfunc=np.sum)
        df_customer_purchase = df_customer_purchase.reset_index()
        df_customer_purchase_prev = df_customer_purchase.shift(1)
        df_customer_purchase_prev["next_month"] = df_customer_purchase["month"]
        df_customer_purchase_prev["interval_month"] = df_customer_purchase_prev["next_month"] - df_customer_purchase_prev["month"]
        df_customer_purchase_prev["consumption_per_month"] = df_customer_purchase_prev["debit"] /df_customer_purchase_prev["interval_month"]
        mean = df_customer_purchase_prev["consumption_per_month"].mean()
        var = df_customer_purchase_prev["consumption_per_month"].var()
        return mean,var
    else:
        return sale_amount / months,0

def get_receivable_term(df_customer_entries,customer_name,receivable_times):
    '''
    获取付款期限的平均值和方差
    :param df_supplier_entries:
    :param supplier_name:
    :param receivable_times:
    :return:
    '''

    if receivable_times >= 2:
        df_supplier_entries = df_customer_entries[
            (df_customer_entries["auxiliary"] != None) & (df_customer_entries["auxiliary"].str.contains(customer_name))]
        df_customer_payment = pd.pivot_table(df_supplier_entries, values=["debit", "credit"], index="month",
                                             aggfunc=np.sum)
        df_customer_payment = df_customer_payment.reset_index()
        df_customer_payment_next = df_customer_payment.shift(1)
        df_customer_payment_next["next_month"] = df_customer_payment["month"]
        df_customer_payment_next["next_debit"] = df_customer_payment["debit"]
        df_customer_payment_next["next_credit"] = df_customer_payment["credit"]
        df_customer_payment_next["term"] = df_customer_payment_next["next_month"] - df_customer_payment_next[
            "month"]
        mean = df_customer_payment_next["term"].mean()
        var = df_customer_payment_next["term"].var()
        return mean, var
    else:
        return 13,0

def get_receivable_balance(df_customer_entries,customer_name,receivable_times):
    if receivable_times >= 2:
        df_customer_entries = df_customer_entries[(df_customer_entries["auxiliary"]!=None) &(df_customer_entries["auxiliary"].str.contains(customer_name))]
        df_customer_payment = pd.pivot_table(df_customer_entries, values=["debit","credit"], index="month",aggfunc=np.sum)
        df_customer_payment = df_customer_payment.reset_index()
        df_customer_payment_next = df_customer_payment.shift(1)
        df_customer_payment_next["next_month"] = df_customer_payment["month"]
        df_customer_payment_next["next_debit"] = df_customer_payment["debit"]
        df_customer_payment_next["next_credit"] = df_customer_payment["credit"]
        df_customer_payment_next["balance"] = df_customer_payment_next["debit"] - df_customer_payment_next["next_debit"]
        mean = df_customer_payment_next["balance"].mean()
        var = df_customer_payment_next["balance"].var()
        return mean,var
    else:
        return 0,0


def save_customer_to_db(session,start_time,end_time):
    '''
    存储客户分析到数据库
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    start_month = start_time.month
    end_month = end_time.month
    months = end_month - start_month + 1

    customer_analysises = session.query(CustomerAnalysis).filter(CustomerAnalysis.start_time == start_time,
                                                                 CustomerAnalysis.end_time == end_time,
                                                            ).all()
    if len(customer_analysises)>0:
        for customer_analysis in customer_analysises:
            session.delete(customer_analysis)
        session.commit()

    customers = get_customers_name(session,start_time,end_time)
    df_transaction_events = get_transaction_events(engine,start_time,end_time)
    for customer_name in set(customers):
        df_customer_entries = get_customer_entry(df_transaction_events, customer_name)
        sale_amount = get_sale_amount(df_customer_entries,customer_name)
        receivable_amount = get_receivable_amount(df_customer_entries,customer_name)
        sale_times = get_sale_times(df_customer_entries,customer_name)
        receivable_times = get_receivable_times(df_customer_entries,customer_name)
        receivable_method = get_receivable_method(df_customer_entries,customer_name)
        sale_amount_per_month = sale_amount / months
        receivable_amount_per_month = receivable_amount / months
        customer_consumption_per_month_average,customer_consumption_per_month_var = get_consumption_per_month(months, df_customer_entries, customer_name, sale_times,sale_amount)
        receivable_term_average,receivable_term_var = get_receivable_term(df_customer_entries, customer_name, receivable_times)
        receivable_balance_average,receivable_balance_var = get_receivable_balance(df_customer_entries, customer_name, receivable_times)
        customer_analysis = CustomerAnalysis(
            start_time=start_time,
            end_time=end_time,
            name=customer_name,
            sale_amount=round(sale_amount,2),
            receivable_amount=round(receivable_amount,2),
            sale_times=sale_times,
            receivable_times=receivable_times,
            receivable_method=receivable_method,
            sale_amount_per_month=round(sale_amount_per_month,2),
            receivable_amount_per_month=round(receivable_amount_per_month,2),
            customer_consumption_per_month_average=round(customer_consumption_per_month_average,2),
            customer_consumption_per_month_var=round(customer_consumption_per_month_var,2),
            receivable_term_average=round(receivable_term_average,2),
            receivable_term_var=round(receivable_term_var,2),
            receivable_balance_average=round(receivable_balance_average,2),
            receivable_balance_var=round(receivable_balance_var,2)
        )
        session.add(customer_analysis)
    session.commit()


def query_customer(session,start_time,end_time):
    '''
    查询客户分析表
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df = pd.read_sql(session.query(CustomerAnalysis).filter(CustomerAnalysis.start_time == start_time,
                                                            CustomerAnalysis.end_time == end_time,
                                                       ).statement, engine)
    records = df.to_json(orient='records')
    sys.stdout.write(records)









if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    query_customer(session, start_time, end_time)


