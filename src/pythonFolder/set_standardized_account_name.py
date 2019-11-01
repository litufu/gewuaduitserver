# -*- coding:utf-8 -*-

import pandas as pd
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Auxiliary, SubjectBalance, ChronologicalAccount,AduitAdjustment,CustomerAnalysis,SupplierAnalysis


def is_auxiliary_conatain(auxiliary,origin_names):
    '''
    检查辅助核算名称是否包含要修改的客户或供应商名称
    :param auxiliary:
    :param origin_names:
    :return:
    '''
    if auxiliary:
        return True in [origin_name in auxiliary for origin_name in origin_names]
    else:
        return False


def change_auxiliary_name(auxiliary,names_contrast):
    '''
    修改辅助核算名称
    :param auxiliary:
    :param names_contrast:
    :return:
    '''
    print(auxiliary)
    print(names_contrast)
    for origin_name in names_contrast:
        if origin_name in auxiliary:
            return auxiliary.replace(origin_name,names_contrast[origin_name])
    return auxiliary

def set_standardized_account_name(session,engine,std_company_names):
    origin_names = [std_company["originName"] for std_company in std_company_names]
    stdNames = [std_company["stdName"] for std_company in std_company_names]
    names_contrast = dict(zip(origin_names, stdNames))
    #1 修改科目余额表
    subject_balances = session.query(SubjectBalance).filter(SubjectBalance.subject_name.in_(origin_names)).all()
    for subject_balance in subject_balances:
        subject_balance.subject_name = names_contrast[subject_balance.subject_name]
    session.commit()
    # 2 修改序时账
    # 修改序时账科目名称
    chronological_accounts = session.query(ChronologicalAccount).filter(ChronologicalAccount.subject_name.in_(origin_names)).all()
    for chronological_account in chronological_accounts:
        chronological_account.subject_name = names_contrast[chronological_account.subject_name]
    session.commit()
    # 修改序时账辅助核算
    df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    df_xsz["is_auxiliary_conatain"] = df_xsz["auxiliary"].apply(is_auxiliary_conatain,args=(origin_names,))
    df_xsz = df_xsz[df_xsz["is_auxiliary_conatain"]==True]
    df_xsz_record = df_xsz[["year","month", "vocher_num", "vocher_type","subentry_num"]]
    replace_records = df_xsz_record.to_dict('records')
    for record in replace_records:
        ca = session.query(ChronologicalAccount).filter(
            ChronologicalAccount.month==record["month"],
            ChronologicalAccount.year==record["year"],
            ChronologicalAccount.vocher_num==record["vocher_num"],
            ChronologicalAccount.vocher_type==record["vocher_type"],
            ChronologicalAccount.subentry_num==record["subentry_num"]
        ).first()
        ca.auxiliary =  change_auxiliary_name(ca.auxiliary, names_contrast)
    session.commit()
    # 3 修改审计调整
    # 修改审计调整科目名称
    aduit_adjustments = session.query(AduitAdjustment).filter(
        AduitAdjustment.subject_name.in_(origin_names)).all()
    for aduit_adjustment in aduit_adjustments:
        aduit_adjustment.subject_name = names_contrast[aduit_adjustment.subject_name]
    session.commit()
    # 修改序时账辅助核算
    df_aduitadjustment = pd.read_sql_table('aduitadjustment', engine)
    df_aduitadjustment["is_auxiliary_conatain"] = df_aduitadjustment["auxiliary"].apply(is_auxiliary_conatain, args=(origin_names,))
    df_aduitadjustment = df_aduitadjustment[df_aduitadjustment["is_auxiliary_conatain"]==True]
    df_aduitadjustment_record = df_aduitadjustment[["year", "month", "vocher_num", "vocher_type", "subentry_num"]]
    replace_records = df_aduitadjustment_record.to_dict('records')
    for record in replace_records:
        ca = session.query(AduitAdjustment).filter(
            AduitAdjustment.month == record["month"],
            AduitAdjustment.year == record["year"],
            AduitAdjustment.vocher_num == record["vocher_num"],
            AduitAdjustment.vocher_type == record["vocher_type"],
            AduitAdjustment.subentry_num == record["subentry_num"]
        ).first()
        ca.auxiliary = change_auxiliary_name(ca.auxiliary, names_contrast)
    session.commit()
    # 4 修改辅助核算
    auxiliaries = session.query(Auxiliary).filter(Auxiliary.name.in_(origin_names)).all()
    for auxiliary in auxiliaries:
        auxiliary.name = names_contrast[auxiliary.name]
    session.commit()
    # 5 修改客户分析
    customers = session.query(CustomerAnalysis).filter(CustomerAnalysis.name.in_(origin_names)).all()
    for customer in customers:
        customer.name = names_contrast[customer.name]
    session.commit()
    # 6 修改供应商分析
    suppliers = session.query(SupplierAnalysis).filter(SupplierAnalysis.name.in_(origin_names)).all()
    for supplier in suppliers:
        supplier.name = names_contrast[supplier.name]
    session.commit()
    sys.stdout.write("success")




if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    std_company_names = json.loads(sys.argv[2])
    # s = '[{"originName":"易德龙电器有限公司","stdName":"苏州易德龙科技股份有限公司"}]'
    # std_company_names = json.loads(s)
    # print(std_company_names)
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    set_standardized_account_name(session,engine,std_company_names)
