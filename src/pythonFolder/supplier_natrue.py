# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database import Auxiliary
from get_tb  import append_all_gradation_subjects
import pandas as pd
from utils import gen_df_line
from constant import inventory,long_term_assets,expense


def get_nature(df_supplier_xsz):
    '''

    :param df_supplier_xsz: 供应商凭证借方
    :return: 供应商属性
    '''
    for i in long_term_assets:
        if df_supplier_xsz["subject_name_1"].str.contains(i).any():
            return "长期资产"
    for i in inventory:
        if df_supplier_xsz["subject_name_1"].str.contains(i).any():
            return "材料费"
    for i in expense:
        if df_supplier_xsz["subject_name_1"].str.contains(i).any():
            return "费用"
    return "材料费"

def add_nature(auxiliaries,df_xsz_last,session):
    '''
    为供应商添加属性
    :param auxiliaries: 供应商
    :param df_xsz_last: 凭证
    :param session: 数据库session
    :return:
    '''
    for auxiliary in auxiliaries:
        df_tmp_xsz = df_xsz_last[(df_xsz_last["auxiliary"].str.contains(auxiliary.name)) & (df_xsz_last["credit"].abs() > 0)]
        if len(df_tmp_xsz) > 0:
            for obj in gen_df_line(df_tmp_xsz.tail(1)):
                df_supplier_xsz = df_xsz_last[
                    (df_xsz_last["month"] == obj["month"]) &
                    (df_xsz_last["vocher_type"] == obj["vocher_type"]) &
                    (df_xsz_last["vocher_num"] == obj["vocher_num"]) &
                    (df_xsz_last["debit"].abs() > 0)
                    ]
                auxiliary.nature = get_nature(df_supplier_xsz)
            session.commit()

def add_supplier_nature(start_time,end_time,session,engine):
    '''
    根据序时账获取辅助核算项目供应商的款项性质
    :param start_time:
    :param end_time:
    :param session:
    :param engine:
    :return:
    '''
    # 获取科目余额表和所有年度序时账
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df_km = pd.read_sql_table('subjectbalance', engine)
    df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]
    df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    df_xsz = append_all_gradation_subjects(df_km, df_xsz)
    # 获取辅助核算中的供应商列表，标明性质
    auxiliaries = session.query(Auxiliary).filter(
        Auxiliary.start_time == start_time,
        Auxiliary.end_time == end_time,
        Auxiliary.type_name == "供应商"
    ).all()
    add_nature(auxiliaries, df_xsz, session)





if __name__ == '__main__':
    # db_path = sys.argv[1]
    db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # start_time = sys.argv[2]
    # end_time = sys.argv[3]
    start_time = "2016-1-1"
    end_time = "2016-12-31"
    add_supplier_nature(start_time, end_time, session, engine)