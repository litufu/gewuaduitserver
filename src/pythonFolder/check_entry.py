import sys
import pandas as pd
import json
from decimal import Decimal
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import TransactionEvent
from constant import monetary_funds,inventory,long_term_assets,expense
from importance import get_actual_importance_level

def deduction_events(session,df_xsz):
    '''
    扣除损益结转项目、存现和取现项目、计提和支付所得税项目、确认递延所得税费用、计提信用减值损失
    :param session:
    :param df_xsz:
    :return:
    '''
    df_xsz = df_xsz.copy()
    df_xsz = df_xsz[
        (df_xsz["desc"]=="损益结转至本年利润")|
        (df_xsz["desc"]=="本年利润结转至利润分配")|
        (df_xsz["desc"]=="银行提取现金")|
        (df_xsz["desc"]=="现金存银行")|
        (df_xsz["desc"]=="银行往来")|
        (df_xsz["desc"]=="支付所得税")|
        (df_xsz["desc"]=="计提所得税") |
        (df_xsz["desc"]=="确认递延所得税费用")|
        (df_xsz["desc"]=="计提信用减值损失")
    ]
    df_xsz_record = df_xsz[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    records = df_xsz_record.to_dict('records')
    for record in records:
        events = get_events_by_record(session, record)
        for event in events:
            event.is_check = False
            event.check_reason = ""
    session.commit()

def get_none_frequent_event(session,df_xsz,actual_importance_level,ratio=0.7,num=5):
    '''
     本期发生笔数少于5笔并且具有重要性的业务
    :param session:
    :param df_xsz:
    :param actual_importance_level:
    :param ratio:
    :param num:
    :return:
    '''
    df_xsz = df_xsz.copy()
    check_start_point = actual_importance_level * ratio
    df_xsz = df_xsz[(df_xsz["entry_classify_count"]<=num)&(df_xsz["transaction_volume"]>check_start_point)]
    df_xsz_record = df_xsz[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    records = df_xsz_record.to_dict('records')
    for record in records:
        events = get_events_by_record(session, record)
        for event in events:
            if (event.is_check != True) and (event.is_check != False):
                event.is_check = True
                event.check_reason = "本期发生笔数少于5笔并且具有重要性的业务"
    session.commit()

def direction_subjects_contain(direction_subjects, subject_list):
    '''
    检查凭证借方是否包含科目列表中的一个科目
    :param direction_subjects: 凭证借方科目或贷方科目列表，str,需要json转换
    :param subject_list: 拟判断的科目列表
    :return: True/False
    '''
    direction_subjects = json.loads(direction_subjects)
    intersaction =  set(direction_subjects) & set(subject_list)
    if len(intersaction) > 0:
        return True
    else:
        return False

def get_events_by_record(session,record):
    '''
    根据凭证编号，获取所有的交易事项描述
    :param session:
    :param record:
    :return:
    '''
    events = session.query(TransactionEvent).filter(
        TransactionEvent.month == record["month"],
        TransactionEvent.vocher_num == record["vocher_num"],
        TransactionEvent.vocher_type == record["vocher_type"],
    ).all()
    return events

def not_pass_payable_account(session,df_xsz,actual_importance_level,ratio=0.7):
    '''
    未通过往来款货币资金直接计入损益（收入、成本、费用）或资产（存货、在建工程、固定资产）等项目
    :param session:
    :param df_xsz:
    :param actual_importance_level:
    :param ratio:
    :return:
    '''
    df_xsz = df_xsz.copy()

    check_start_point = actual_importance_level * ratio
    df_xsz = df_xsz[(df_xsz["transaction_volume"]>check_start_point)]
#     购置资产或发生成本费用，未通过往来款核算,贷方为货币资金，借方为资产或费用
    assets_and_fees = [*inventory,*long_term_assets,*expense]
    df_xsz_assets_and_fees = df_xsz[
        (df_xsz["opposite_subjects"].apply(direction_subjects_contain,args=(tuple(monetary_funds),)))&
        (df_xsz["same_subjects"].apply(direction_subjects_contain,args=(tuple(assets_and_fees),)))
    ]
    df_xsz_assets_and_fees_record = df_xsz_assets_and_fees[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    df_xsz_assets_and_fees_records = df_xsz_assets_and_fees_record.to_dict('records')
    for record in df_xsz_assets_and_fees_records:
        events = get_events_by_record(session, record)
        for event in events:
            if (event.is_check != True) and (event.is_check != False):
                event.is_check = True
                event.check_reason = "未通过往来款核算直接计入资产或费用"
    session.commit()
#         未通过往来款核算直接计入收入
    income_subjects = ["主营业务收入","其他业务收入"]
    df_xsz_income = df_xsz[
        (df_xsz["opposite_subjects"].apply(direction_subjects_contain, args=(tuple(income_subjects),))) &
        (df_xsz["same_subjects"].apply(direction_subjects_contain, args=(tuple(monetary_funds),)))
        ]
    df_xsz_income = df_xsz_income[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    df_xsz_income_records = df_xsz_income.to_dict('records')
    for record in df_xsz_income_records:
        events = get_events_by_record(session,record)
        for event in events:
            if (event.is_check != True) and (event.is_check != False):
                event.is_check = True
                event.check_reason = "未通过往来款核算直接计入收入"
    session.commit()


def clean_check(session,df_xsz):
    df_xsz_records = df_xsz.to_dict('records')
    for record in df_xsz_records:
        events = get_events_by_record(session, record)
        for event in events:
            if (event.is_check == True) or (event.is_check == False):
                event.is_check = None
                event.check_reason = None
    session.commit()


def adjustment_bussiness(session,df_xsz,actual_importance_level,ratio=0.7,integer_num=4):
    '''
    检查是否为调整类凭证
    :param session:
    :param df_xsz:
    :param actual_importance_level:
    :param ratio:
    :param integer_num:
    :return:
    '''
    df_xsz = df_xsz.copy()
    check_start_point = actual_importance_level * ratio
    df_xsz = df_xsz[(df_xsz["transaction_volume"] > check_start_point)]
    df_xsz = df_xsz[
        (df_xsz["description"].str.contains("调整"))|
        (df_xsz["description"].str.contains("冲销"))|
        (df_xsz["description"].str.contains("冲减"))
    ]
    df_xsz_records = df_xsz.to_dict('records')
    for record in df_xsz_records:
        events = get_events_by_record(session, record)
        for event in events:
            if (event.is_check != True) and (event.is_check != False):
                event.is_check = True
                event.check_reason = "大额调整凭证".format(integer_num)
    session.commit()



def integer_bussiness(session,df_xsz,actual_importance_level,ratio=0.7,integer_num=4):
    '''
    金额为整数的交易或业务
    :param session:
    :param df_xsz:
    :param actual_importance_level:
    :param ratio:
    :param integer_num:整数位数
    :return:
    '''
    integer_num_contrast = {4:"整万",3:"整千",2:"整百"}
    df_xsz= df_xsz.copy()
    check_start_point = actual_importance_level * ratio
    df_xsz = df_xsz[(df_xsz["transaction_volume"] > check_start_point)]
    df_xsz["bussiness_amount"] = df_xsz["transaction_volume"]/(10**integer_num)
    df_xsz["is_integer_bussiness"] = df_xsz["bussiness_amount"].apply(check_last_two_num_after_dot)
    df_xsz = df_xsz[df_xsz["is_integer_bussiness"]==True]
    df_xsz_records = df_xsz.to_dict('records')
    for record in df_xsz_records:
        events = get_events_by_record(session, record)
        for event in events:
            if (event.is_check != True) and (event.is_check != False):
                event.is_check = True
                event.check_reason = "交易金额后为{}的分录".format(integer_num_contrast[integer_num])
    session.commit()


def check_last_two_num_after_dot(x):
    '''
    检查是不是整数万，整千或整百
    :param x:
    :return:
    '''
    return str(Decimal.from_float(x).quantize(Decimal('0.0000')))[-4:] == "0000"

def output_check_entry(start_time,end_time,engine):
    year = start_time.year
    start_month = start_time.month
    end_month = end_time.month
    df_xsz = pd.read_sql_table("transactionevent", engine)
    df_transactionevent = df_xsz[(df_xsz['year'] == year) & (df_xsz['month'] >= start_month) & (df_xsz['month'] <= end_month)  & (df_xsz['is_check'] == True)]
    df_xsz_new = df_transactionevent[
        [ "month", "vocher_type", "vocher_num",  "description", "subject_num", "subject_name",
         "debit", "credit", "auxiliary","check_reason","tb_subject"]]
    sys.stdout.write(df_xsz_new.to_json(orient='records'))


def check_entry(start_time,end_time,actual_importance_level,ratio,num,integer_num,recompute,engine,session):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    year = start_time.year
    start_month = start_time.month
    end_month = end_time.month
    df_xsz = pd.read_sql_table("transactionevent", engine)
    df_xsz = df_xsz[(df_xsz['year'] == year) & (df_xsz['month'] >= start_month) & (df_xsz['month'] <= end_month)]
    df_xsz_check = df_xsz[df_xsz["is_check"]==True]
    if len(df_xsz_check)>0:
        if recompute == "yes":
            clean_check(session, df_xsz)
            deduction_events(session,df_xsz)
            get_none_frequent_event(session,df_xsz,actual_importance_level,ratio,num)
            not_pass_payable_account(session, df_xsz, actual_importance_level, ratio)
            integer_bussiness(session, df_xsz, actual_importance_level, ratio, integer_num)
            output_check_entry(start_time,end_time,engine)
        else:
            output_check_entry(start_time, end_time,engine)
    else:
        clean_check(session, df_xsz)
        deduction_events(session, df_xsz)
        get_none_frequent_event(session, df_xsz, actual_importance_level, ratio, num)
        not_pass_payable_account(session, df_xsz, actual_importance_level, ratio)
        integer_bussiness(session, df_xsz, actual_importance_level, ratio, integer_num)
        output_check_entry(start_time, end_time,engine)



if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    ratio = float(sys.argv[4])
    num = int(sys.argv[5])
    integer_num = int(sys.argv[6])
    recompute = sys.argv[7]
    company_type = sys.argv[8]
    #
    # db_path = "D:\gewuaduit\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    from utils import add_suggestion
    # companyname = "深圳市众恒世讯科技股份有限公司"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # ratio = 0.7
    # num = 5
    # integer_num = 4
    # recompute = "yes"
    # company_type = "其他公司"
    actual_importance_level = int(get_actual_importance_level(company_type, start_time, end_time, engine, session,
                                                          add_suggestion))
    check_entry(start_time,end_time,actual_importance_level,ratio,num,integer_num,recompute,engine,session)