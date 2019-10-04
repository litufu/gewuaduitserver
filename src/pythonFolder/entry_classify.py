# -*- coding:utf-8 -*-

from collections import defaultdict
import json
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database import EntryClassify
from get_tb  import get_new_km_xsz_df
from utils import gen_df_line


def get_entry_subjects(df_one_entry,subject_name_grade):
    '''
    获取凭证的借贷方科目
    :param df_one_entry: 一笔凭证
    :return: 借方科目列表和贷方科目列表组成的字典{"debit":debit_subjects_list,"credit":credit_subjects_list}
    '''
    debit_subjects = set()
    credit_subjects = set()
    # 获取凭证的借贷方
    for obj in gen_df_line(df_one_entry):
        if obj["debit"] > 1e-5:
            debit_subjects.add(obj[subject_name_grade])
        else:
            credit_subjects.add((obj[subject_name_grade]))

    debit_subjects_list = list(debit_subjects)
    credit_subjects_list = list(credit_subjects)
    debit_subjects_list.sort()
    credit_subjects_list.sort()

    return {"debit":debit_subjects_list,"credit":credit_subjects_list}


def output_entryclassify(engine,start_time,end_time):
    start_time_format = datetime.strptime(start_time, '%Y-%m-%d')
    end_time_format = datetime.strptime(end_time, '%Y-%m-%d')
    df_entryclassify = pd.read_sql_table('entryclassify', engine)
    df_entryclassify = df_entryclassify[
        (df_entryclassify['start_time'] == start_time_format) & (df_entryclassify['end_time'] == end_time_format)]
    df_entryclassify_new = df_entryclassify[
        ['desc', "value", 'number', 'records']]
    sys.stdout.write(df_entryclassify_new.to_json(orient='records'))

def compute(start_time,end_time,session,engine,add_suggestion):
    # 获取科目余额表和序时账
    df_km, df_xsz = get_new_km_xsz_df(start_time, end_time,"unAudited", engine, add_suggestion, session)
    # 获取所有的凭证记录
    df_xsz_record = df_xsz[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    records = df_xsz_record.to_dict('records')
    # 1/按照借方和贷方分类
    dict_tmp = defaultdict(list)
    dict_tmp_value = defaultdict(float)
    for record in records:
        # 获取每一笔凭证
        df_tmp = df_xsz[(df_xsz["month"] == record["month"])
                        & (df_xsz["vocher_num"] == record["vocher_num"])
                        & (df_xsz["vocher_type"] == record["vocher_type"])
                        ]
        value = df_tmp["debit"].sum()
        # 获取凭证的借方和贷方一级科目名称
        subjects = get_entry_subjects(df_tmp, "subject_name_1")
        debit_subjects_list = subjects["debit"]
        credit_subjects_list = subjects["credit"]
        # 合并科目名称
        debit_subject_desc = "%".join(debit_subjects_list)
        credit_subjects_desc = "%".join(credit_subjects_list)
        entry_desc = debit_subject_desc + "@" + credit_subjects_desc
        dict_tmp[entry_desc].append((record["month"], record["vocher_num"], record["vocher_type"]))
        dict_tmp_value[entry_desc] = dict_tmp_value[entry_desc] + value

    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')

    for key in dict_tmp:
        entryclassify = EntryClassify(
            start_time=start_time,
            end_time=end_time,
            step=1,
            desc=key,
            value=dict_tmp_value[key],
            number=len(dict_tmp[key]),
            records=json.dumps(dict_tmp[key], ensure_ascii=False)
        )
        session.add(entryclassify)
    session.commit()

def get_entry_classifies(start_time,end_time,session):
    start_time_format = datetime.strptime(start_time, '%Y-%m-%d')
    end_time_format = datetime.strptime(end_time, '%Y-%m-%d')
    entry_classfies = session.query(EntryClassify).filter(EntryClassify.start_time == start_time_format,
                                                          EntryClassify.end_time == end_time_format).all()
    return entry_classfies


def analyse_entry(start_time,end_time,session,engine,add_suggestion,recompute):
    entry_classfies = get_entry_classifies(start_time,end_time,session)
    if len(entry_classfies) > 0:
        if recompute == "yes":
            for entry_classify in entry_classfies:
                session.delete(entry_classify)
            session.commit()
            compute(start_time, end_time, session, engine, add_suggestion)
            output_entryclassify(engine, start_time, end_time)
        else:
            output_entryclassify(engine,start_time,end_time)
    else:
        compute(start_time, end_time, session, engine, add_suggestion)
        output_entryclassify(engine, start_time, end_time)


if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    recompute=sys.argv[4]
    # db_path = "D:\gewuaduit\server\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    from utils import add_suggestion

    # companyname = "深圳市众恒世讯科技股份有限公司"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # recompute="no"
    # recalculation(start_time,end_time,type,engine,add_suggestion,session)

    analyse_entry(start_time,end_time,session,engine,add_suggestion,recompute)

