import sys
import pandas as pd
import numpy as np
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary,SupplierAnalysis,TransactionEvent




# 1、目的：寻找到异常的供应商
# 供应商付款方式：汇票、银行、现金。检查是否有异常付款方式的供应商。
# 供应商付款时间：采购与付款之间的间隔。检查给予的信用期间是否发生明显的变化。
# 供应商付款金额：采购金额与付款金额之间的差异。检查公司是否已足额支付了上次的欠款。
# 供应商采购时间：根据采购金额、两次采购之间的间隔，计算每次采购后大概的每日消耗金额。检查是否存在大额存货的情况下依旧采购。
# 2、供应商分析流程：
# 2.1从辅助核算中获取供应商名录
# 2.2获取所有与供应商有关的（应付、预付）凭证
# 2.3年度采购金额
# 年度付款金额
# 年度采购次数
# 年度付款次数
# 付款方式统计表（现金、银行存款、应收票据、应付票据、其他）
#获取月度采购金额
#获取月度付款金额
#本月采购与下一次采购之间相差的月份
# 本月采购后每月消耗金额
# 月度消耗金额平均值
# 月耗方差和标准差
# 本月采购与下次付款之间时间差异
# 采购和下次付款时间差平均值
# 采购和下次付款时间差方差和标准层
# 本月采购金额与下次付款金额之间的差异
# 本月采购金额与下次付款金额之间的差异平均值
# 本月采购金额与下次付款金额之间的差异方差和标准层
# 3、相关字段名：
# 供应商名称。本期采购金额、本期付款金额、本期采购次数、本期付款次数、本期付款方式、月度平均采购额、月度平均付款额、月耗平均值、月耗方差、付款期限平均值、付款期限方差、付款差额平均值、付款差额方差
# 4、计算公式
#本期采购金额 = 应付预付账款贷方发生额
#本期付款金额 = 应付预付账款借方发生额
# 本期采购次数 = 应付预付贷方发生次数
# 本期付款次数 = 应付预付借方发生次数
# 本期付款方式 = 应付预付借方时，对方科目名称是银行存款、应付账款、现金、应收票据、应付账款等
# 月度平均采购额 = 本期采购金额/本期月数
# 月度平均付款额 = 本期付款金额 /本期月数
# 月耗平均值 = sum（本次采购 /本次采购与下次采购相差的月份/（采购次数-1）
# 月耗方差 = sum(（月耗-平均值）**2)/(采购次数-1）
# 付款期限平均值 = sum(本次采购与下次付款期间相差月份）/（付款次数-1）
# 付款期限方差 = sum(（付款期限-平均值）**2)/(付款次数-1）
# 付款差额平均值 = sum(本次采购金额与下次付款金额差额）/(付款次数-1）
# 付款差额方差 = sum(（付款差额-平均值）**2)/(付款次数-1）


def get_suppliers_name(engine,session,start_time,end_time):
    '''
    2.1从辅助核算中获取供应商名录
    :param session:
    :param start_time:
    :param end_time:
    :return:
    '''
    suppliers = []
    auxiliaries = session.query(Auxiliary).filter(Auxiliary.start_time==start_time,Auxiliary.end_time==end_time).all()
    for auxiliary in auxiliaries:
        if "供应商" in auxiliary.type_name:
            suppliers.append(auxiliary.name)
    return suppliers


def get_transaction_events(engine,session,start_time,end_time):
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

def get_supplier_entry(df_transactionEvent,supplier_name):
    '''
    2.2根据序时账和供应商名称，筛选出所有的供应商凭证
    :param df_transactionEvent:序时账
    :param supplier_name:供应商名称
    :return:获取所有与供应商有关的（应付、预付）凭证
    '''
    df_supplier_transactionEvent = df_transactionEvent[(df_transactionEvent["auxiliary"].str.contains(supplier_name))&
                                              (df_transactionEvent["tb_subject"].isin(["应付账款","预付款项"]))]
    df_supplier_record = df_supplier_transactionEvent[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    # 获取相反凭证的完整借贷方
    df_supplier_entries = pd.merge(df_transactionEvent, df_supplier_record, how="inner",
                                     on=["month", "vocher_num", "vocher_type"])
    return df_supplier_entries


def get_puchase_amount(df_supplier_entries,supplier_name):
    '''
    获取本期从供应商购买的金额
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:
    '''
    # 获取贷方大于0的，包含供应商名称的行
    df_supplier_entries = df_supplier_entries[
        (df_supplier_entries["auxiliary"].str.contains(supplier_name))&
        (df_supplier_entries["credit"].abs()>0)
    ]
    return df_supplier_entries["credit"].sum()

def get_puchase_times(df_supplier_entries,supplier_name):
    '''
    获取本期从供应商购买的次数
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:
    '''
    # 获取贷方大于0的，包含供应商名称的行
    df_supplier_entries = df_supplier_entries[
        (df_supplier_entries["auxiliary"].str.contains(supplier_name))&
        (df_supplier_entries["credit"].abs()>0)
    ]
    return len(df_supplier_entries)

def get_payment_amount(df_supplier_entries,supplier_name):
    '''
    获取本期付给供应商的金额
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:
    '''
    # 获取贷方大于0的，包含供应商名称的行
    df_supplier_entries = df_supplier_entries[
        (df_supplier_entries["auxiliary"].str.contains(supplier_name))&
        (df_supplier_entries["debit"].abs()>0)
    ]
    return df_supplier_entries["debit"].sum()

def get_payment_times(df_supplier_entries,supplier_name):
    '''
    获取本期付给供应商的次数
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:
    '''
    # 获取贷方大于0的，包含供应商名称的行
    df_supplier_entries = df_supplier_entries[
        (df_supplier_entries["auxiliary"].str.contains(supplier_name))&
        (df_supplier_entries["debit"].abs()>0)
    ]
    return len(df_supplier_entries["debit"])

def get_payment_method(df_supplier_entries,supplier_name):
    '''
    获取本期付给供应商的付款方式
    :param df_supplier_entries:供应商凭证
    :param supplier_name:供应商名称
    :return:"银行存款、库存现金、应收票据、应付票据
    '''
    methods_set = {"银行存款","库存现金","应收票据","应付票据"}
    # 获取借方大于0的，包含供应商名称的行
    df_supplier_entries = df_supplier_entries[
        (df_supplier_entries["auxiliary"].str.contains(supplier_name))&
        (df_supplier_entries["debit"].abs()>0)
    ]
    subjects = []
    for opposite_subjects in df_supplier_entries["opposite_subjects"].to_list():
        tmp = json.loads(opposite_subjects)
        subjects.extend(tmp)
    subjects_set = set(subjects)
    methods = list(methods_set.intersection(subjects_set))
    methods.sort()
    method = "、".join(methods)
    return method

def get_consumption_per_month(months,df_supplier_entries,supplier_name,purchase_times,purchase_amount):
    '''
    获取每月消耗平均数和方差
    :param months:本期月份数
    :param df_supplier_entries:
    :param supplier_name:
    :param purchase_times:
    :param purchase_amount:
    :return:
    '''


    if purchase_times >= 2:
        df_supplier_entries = df_supplier_entries[
            (df_supplier_entries["auxiliary"].str.contains(supplier_name)) &
            (df_supplier_entries["credit"].abs() > 0)
        ]
        df_supplier_purchase = pd.pivot_table(df_supplier_entries, values="credit", index="month",aggfunc=np.sum)
        df_supplier_purchase = df_supplier_purchase.reset_index()
        df_supplier_purchase_prev = df_supplier_purchase.shift(1)
        df_supplier_purchase_prev["next_month"] = df_supplier_purchase["month"]
        df_supplier_purchase_prev["interval_month"] = df_supplier_purchase_prev["next_month"] - df_supplier_purchase_prev["month"]
        df_supplier_purchase_prev["consumption_per_month"] = df_supplier_purchase_prev["credit"] /df_supplier_purchase_prev["interval_month"]
        mean = df_supplier_purchase_prev["consumption_per_month"].mean()
        var = df_supplier_purchase_prev["consumption_per_month"].var()
        return mean,var
    else:
        return purchase_amount / months,0

def get_payment_term(df_supplier_entries,supplier_name,payment_times):
    '''
    获取付款期限的平均值和方差
    :param df_supplier_entries:
    :param supplier_name:
    :param payment_times:
    :return:
    '''

    if payment_times >= 2:
        df_supplier_entries = df_supplier_entries[
            (df_supplier_entries["auxiliary"] != None) & (df_supplier_entries["auxiliary"].str.contains(supplier_name))]
        df_supplier_payment = pd.pivot_table(df_supplier_entries, values=["debit", "credit"], index="month",
                                             aggfunc=np.sum)
        df_supplier_payment = df_supplier_payment.reset_index()
        df_supplier_payment_next = df_supplier_payment.shift(1)
        df_supplier_payment_next["next_month"] = df_supplier_payment["month"]
        df_supplier_payment_next["next_debit"] = df_supplier_payment["debit"]
        df_supplier_payment_next["next_credit"] = df_supplier_payment["credit"]
        df_supplier_payment_next["term"] = df_supplier_payment_next["next_month"] - df_supplier_payment_next[
            "month"]
        mean = df_supplier_payment_next["term"].mean()
        var = df_supplier_payment_next["term"].var()
        return mean, var
    else:
        return 13,0

def get_payment_balance(df_supplier_entries,supplier_name,payment_times):
    if payment_times >= 2:
        df_supplier_entries = df_supplier_entries[(df_supplier_entries["auxiliary"]!=None) &(df_supplier_entries["auxiliary"].str.contains(supplier_name))]
        df_supplier_payment = pd.pivot_table(df_supplier_entries, values=["debit","credit"], index="month",aggfunc=np.sum)
        df_supplier_payment = df_supplier_payment.reset_index()
        df_supplier_payment_next = df_supplier_payment.shift(1)
        df_supplier_payment_next["next_month"] = df_supplier_payment["month"]
        df_supplier_payment_next["next_debit"] = df_supplier_payment["debit"]
        df_supplier_payment_next["next_credit"] = df_supplier_payment["credit"]
        df_supplier_payment_next["balance"] = df_supplier_payment_next["credit"] - df_supplier_payment_next["next_debit"]
        mean = df_supplier_payment_next["balance"].mean()
        var = df_supplier_payment_next["balance"].var()
        return mean,var
    else:
        return 0,0


def save_supplier_to_db(engine,session,start_time,end_time):
    '''
    存储供应商分析到数据库
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

    supplier_analysises = session.query(SupplierAnalysis).filter(SupplierAnalysis.start_time == start_time,
                                                            SupplierAnalysis.end_time == end_time,
                                                            ).all()
    if len(supplier_analysises)>0:
        for supplier_analysis in supplier_analysises:
            session.delete(supplier_analysis)
        session.commit()



    suppliers = get_suppliers_name(engine,session,start_time,end_time)
    df_transaction_events = get_transaction_events(engine,session,start_time,end_time)
    for supplier_name in set(suppliers):
        df_supplier_entries = get_supplier_entry(df_transaction_events, supplier_name)
        purchase_amount = get_puchase_amount(df_supplier_entries,supplier_name)
        payment_amount = get_payment_amount(df_supplier_entries,supplier_name)
        purchase_times = get_puchase_times(df_supplier_entries,supplier_name)
        payment_times = get_payment_times(df_supplier_entries,supplier_name)
        purchase_method = get_payment_method(df_supplier_entries,supplier_name)
        purchase_amount_per_month = purchase_amount / months
        payment_amount_per_month = payment_amount / months
        consumption_per_month_average,consumption_per_month_var = get_consumption_per_month(months, df_supplier_entries, supplier_name, purchase_times,
                                      purchase_amount)
        payment_term_average,payment_term_var = get_payment_term(df_supplier_entries, supplier_name, payment_times)
        payment_balance_average,payment_balance_var = get_payment_balance(df_supplier_entries, supplier_name, payment_times)
        supplier_analysis = SupplierAnalysis(
            start_time=start_time,
            end_time=end_time,
            name=supplier_name,
            purchase_amount=round(purchase_amount,2),
            payment_amount=round(payment_amount,2),
            purchase_times=purchase_times,
            payment_times=payment_times,
            purchase_method=purchase_method,
            purchase_amount_per_month=round(purchase_amount_per_month,2),
            payment_amount_per_month=round(payment_amount_per_month,2),
            consumption_per_month_average=round(consumption_per_month_average,2),
            consumption_per_month_var=round(consumption_per_month_var,2),
            payment_term_average=round(payment_term_average,2),
            payment_term_var=round(payment_term_var,2),
            payment_balance_average=round(payment_balance_average,2),
            payment_balance_var=round(payment_balance_var,2)
        )
        session.add(supplier_analysis)
    session.commit()


def query_supplier(start_time,end_time,session):
    '''
    查询供应商分析表
    :param start_time:
    :param end_time:
    :return:
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df = pd.read_sql(session.query(SupplierAnalysis).filter(SupplierAnalysis.start_time == start_time,
                                                       SupplierAnalysis.end_time == end_time,
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
    query_supplier(start_time, end_time, session)


