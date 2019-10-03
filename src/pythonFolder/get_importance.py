# -*- coding:utf-8 -*-
import pandas as pd
import math
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from get_tb import get_new_km_xsz_df,get_tb
from database import SubjectContrast, TBSubject,TB
from utils import gen_df_line, check_start_end_date, get_session_and_engine, \
    get_subject_num_by_name, get_subject_value_by_name, get_detail_subject_df, get_xsz_by_subject_num, \
    get_subject_num_by_similar_name, get_not_null_df_km, get_subject_value_by_num,CJsonEncoder,get_tb_origin_value



def importance_level(company_nature,pre_tax_profit,income,net_assets,total_assets,mini_level=50000):
    '''

    :param company_nature: 公司类型：上市公司、拟上市公司、国有企业，其他公司
    :param pre_tax_profit: 税前利润金额
    :param income: 收入金额
    :param net_assets: 净资产金额
    :param total_assets: 总资产金额
    :param mini_level: 事务所报表整体最低重要性水平
    :return:
    metrological_basis：计量基础
    metrological_basis_value：计量基础金额
    overall_report_form_level_ratio：报表整体重要性水平比例
    actual_importance_level_ratio：实际执行重要性水平比例
    uncorrected_misstatement：未更正错报名义金额比例
    '''

    if company_nature == "上市公司" or company_nature == "拟上市公司" :
        if pre_tax_profit * 0.05 > mini_level:
            metrological_basis = "税前利润"
            metrological_basis_value = pre_tax_profit
            overall_report_form_level_ratio = 0.05
        elif income * 0.005 > mini_level:
            metrological_basis = "营业收入"
            metrological_basis_value = income
            overall_report_form_level_ratio = 0.005
        elif net_assets * 0.01 > mini_level:
            metrological_basis = "净资产"
            metrological_basis_value = net_assets
            overall_report_form_level_ratio = 0.01
        elif net_assets * 0.0025 > mini_level:
            metrological_basis = "总资产"
            metrological_basis_value = total_assets
            overall_report_form_level_ratio = 0.0025
        else:
            metrological_basis = "事务所最低财务报表整体重要性水平"
            metrological_basis_value = mini_level
            overall_report_form_level_ratio = 1
        actual_importance_level_ratio = 0.5
        uncorrected_misstatement = 0.05
    elif company_nature == "国有企业":
        if pre_tax_profit * 0.06 > mini_level:
            metrological_basis = "税前利润"
            metrological_basis_value = pre_tax_profit
            overall_report_form_level_ratio = 0.06
        elif income * 0.0075 > mini_level:
            metrological_basis = "营业收入"
            metrological_basis_value = income
            overall_report_form_level_ratio =  0.0075
        elif net_assets * 0.03 > mini_level:
            metrological_basis = "净资产"
            metrological_basis_value = net_assets
            overall_report_form_level_ratio = 0.03
        elif net_assets * 0.0035 > mini_level:
            metrological_basis = "总资产"
            metrological_basis_value = total_assets
            overall_report_form_level_ratio = 0.0035
        else:
            metrological_basis = "事务所最低财务报表整体重要性水平"
            metrological_basis_value = mini_level
            overall_report_form_level_ratio = 1
        actual_importance_level_ratio = 0.75
        uncorrected_misstatement = 0.03
    else:
        if pre_tax_profit * 0.08 > mini_level:
            metrological_basis = "税前利润"
            metrological_basis_value = pre_tax_profit
            overall_report_form_level_ratio = 0.08
        elif income * 0.01 > mini_level:
            metrological_basis = "营业收入"
            metrological_basis_value = income
            overall_report_form_level_ratio =  0.01
        elif net_assets * 0.05 > mini_level:
            metrological_basis = "净资产"
            metrological_basis_value = net_assets
            overall_report_form_level_ratio = 0.05
        elif net_assets * 0.005 > mini_level:
            metrological_basis = "总资产"
            metrological_basis_value = total_assets
            overall_report_form_level_ratio = 0.005
        else:
            metrological_basis = "事务所最低财务报表整体重要性水平"
            metrological_basis_value = mini_level
            overall_report_form_level_ratio = 1
        actual_importance_level_ratio = 0.75
        uncorrected_misstatement = 0.03
    res = {
        "metrologicalBasis":metrological_basis,
        "metrologicalBasisValue":metrological_basis_value,
        "overallReportFormLevelRatio":overall_report_form_level_ratio,
        "actualImportanceLevelRatio":actual_importance_level_ratio,
        "uncorrectedMisstatement":uncorrected_misstatement,
        "companyNature":company_nature
    }
    return res

def get_subject_value(df_tb,subject_str):
    subject_df = df_tb[df_tb["show"].str.contains(subject_str)]
    if len(subject_df) == 1:
        subject_value = subject_df["amount"].values[0]
    else:
        subject_value = 0.00
    return subject_value

if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    company_nature=sys.argv[4]
    type = "audited"
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    # companyname = "深圳市众恒世讯科技股份有限公司"
    # start_time = "2015-1-1"
    # end_time = "2015-12-31"
    # company_type="其他公司"

    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    from utils import add_suggestion
    # 根据序时账和科目余额表重新计算新的科目余额表和序时账，主要是损益核算方向的检查
    df_km_new, df_xsz_new = get_new_km_xsz_df(start_time, end_time, type, engine, add_suggestion, session)
    # 根据新的科目余额表计算tb
    df_tb = get_tb(df_km_new, df_xsz_new, engine, add_suggestion, start_time, end_time)
    df_tb = df_tb.reset_index()
    df_tb = df_tb[["show", "amount", "order", "direction"]]
    pre_tax_profit = get_subject_value(df_tb,"四、利润总额")
    income = get_subject_value(df_tb,"一、营业总收入")
    net_assets = get_subject_value(df_tb,"股东权益合计")
    total_assets = get_subject_value(df_tb,"资产总计")
    res = importance_level(company_nature,pre_tax_profit,income,net_assets,total_assets)
    sys.stdout.write(json.dumps(res))



