# -*- coding:utf-8 -*-

import pandas as pd
import math
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SubjectContrast, TBSubject,TB
from utils import gen_df_line, check_start_end_date, get_session_and_engine, \
    get_subject_num_by_name, get_subject_value_by_name, get_detail_subject_df, get_xsz_by_subject_num, \
    get_subject_num_by_similar_name, get_not_null_df_km, get_subject_value_by_num,CJsonEncoder,get_tb_origin_value


# 通过科目余额表和序时账生成TB
# 步骤：
# 1/通过科目余额表期初数和序时账重新计算期末数和损益发生额
# 2/将重新计算生成的科目余额表按照科目与TB对照表生成TB


def modify_tb(show, add_subject_name, sign, session):
    objs = session.query(TBSubject).filter(TBSubject.show.like('%{}'.format(show))).all()
    obj = [obj for obj in objs if obj.show.strip() == show][0]
    obj_subject = obj.subject
    obj.subject = obj_subject + "{}%{}%".format(sign, add_subject_name)

def modify_all_tb(shows, add_subject_name, sign, session):
    for show in shows:
        modify_tb(show, add_subject_name, sign, session)

def add_std_not_exist_subject(df_km, df_std, session):
    '''
    实现步骤：
    按照科目编码对科目余额表进行升序排列
    # 资产判断
    #如果在流动资产内，则为流动资产
    # 如果在所有流动资产之后，在所有非流动资产之前，分类为流动资产
    # 如果在非流动资产内，则为非流动资产
    # 负债判断
    # 同流动资产和非流动资产
    # 权益类
    # 收入类
    # 成本费用类
    :param df_km:
    :param df_std:
    :return:同时修改TBsubject和subject_contrast
    '''
    df_km = df_km.copy()
    df_std = df_std.copy()

    # 按照科目编码对科目余额表进行升序排列
    df_km = df_km.sort_values(by=['subject_num'])
    std_not_match_subject = {"坏账准备", "本年利润", "利润分配", "以前年度损益调整"}
    # 获取一级科目余额表，用于检查是否存在未识别的一级科目，且至少在期初/期末或本期借贷方有发生额
    df_km_first_subject = get_not_null_df_km(df_km, 1)
    # 检查是否有未识别的一级会计科目
    df_km_first_subject_merge_std = pd.merge(df_km_first_subject, df_std, how="left", left_on='subject_name',
                                             right_on="origin_subject")
    df_km_first_subject_not_match = df_km_first_subject_merge_std[df_km_first_subject_merge_std['coefficient'].isna()]
    diff_subject_names = set(df_km_first_subject_not_match['subject_name'])
    res_diff_subject_names = diff_subject_names - std_not_match_subject
    if len(res_diff_subject_names) == 0:
        # 没有未匹配的以及科目
        return
    # 遍历每一个标准科目表中不存在的科目，分别增加科目对照表和TBSubject
    for obj in gen_df_line(df_km_first_subject_not_match):
        if obj["subject_name"] in std_not_match_subject:
            continue
        index_num = df_km_first_subject_merge_std[
            df_km_first_subject_merge_std["subject_name"] == obj["subject_name"]].index.values[0]
        last_class = df_km_first_subject_merge_std.at[index_num - 1, "second_class"]
        next_class = df_km_first_subject_merge_std.at[index_num + 1, "second_class"]
        if obj["subject_type"] == "资产":
            if (next_class == "流动资产") or (next_class == "非流动资产" and last_class == "流动资产"):
                this_class = "流动资产"
                tb_obj = session.query(TBSubject).filter(TBSubject.order > 100, TBSubject.order < 200).order_by(
                    TBSubject.order.desc()).first()
                order = tb_obj.order
                #     增加流动资产和总资产
                modify_subjects = ["流动资产合计", "资产总计"]
                if obj["direction_x"] == "借":
                    modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                else:
                    modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            else:
                this_class = "非流动资产"
                tb_obj = session.query(TBSubject).filter(TBSubject.order > 200, TBSubject.order < 300).order_by(
                    TBSubject.order.desc()).first()
                order = tb_obj.order
                #     增加非流动资产和总资产
                modify_subjects = ["非流动资产合计", "资产总计"]
                if obj["direction_x"] == "借":
                    modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                else:
                    modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            first_class = "资产"
        elif obj["subject_type"] == "负债":
            if (next_class == "流动负债") or (next_class == "非流动负债" and last_class == "非流动负债"):
                this_class = "流动负债"
                tb_obj = session.query(TBSubject).filter(TBSubject.order > 300, TBSubject.order < 400).order_by(
                    TBSubject.order.desc()).first()
                order = tb_obj.order
                #     增加流动负债和总负债/负债和所有者权益
                modify_subjects = ["流动负债合计", "负债合计", "负债和股东权益总计"]
                if obj["direction_x"] == "贷":
                    modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                else:
                    modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            else:
                this_class = "非流动负债"
                tb_obj = session.query(TBSubject).filter(TBSubject.order > 400, TBSubject.order < 500).order_by(
                    TBSubject.order.desc()).first()
                order = tb_obj.order
                #          增加非流动负债和总负债/负债和所有者权益
                modify_subjects = ["非流动负债合计", "负债合计", "负债和股东权益总计"]
                if obj["direction_x"] == "贷":
                    modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                else:
                    modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            first_class = "负债"
        elif obj["subject_type"] == "权益":
            if ("股本" in obj['subject_name']) or ("实收资本" in obj["subject_name"]):
                subjectcontrast = SubjectContrast(origin_subject=obj["subject_name"], tb_subject="股本(实收资本）",
                                                  fs_subject="股本", coefficient=1, direction="贷",
                                                  first_class="权益", second_class="所有者权益")
                session.add(subjectcontrast)
                session.commit()
                continue
            this_class = "所有者权益"
            first_class = "权益"
            tb_obj = session.query(TBSubject).filter(TBSubject.order > 500, TBSubject.order < 600).order_by(
                TBSubject.order.desc()).first()
            order = tb_obj.order
            #     增加所有者权益和负债和所有者权益
            modify_subjects = ["归属于母公司股东权益合计", "股东权益合计", "负债和股东权益总计"]
            if obj["direction_x"] == "贷":
                modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
            else:
                modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
        elif obj["subject_type"] == "成本":
            this_class = "流动资产"
            first_class = "资产"
            tb_obj = session.query(TBSubject).filter(TBSubject.order > 100, TBSubject.order < 200).order_by(
                TBSubject.order.desc()).first()
            order = tb_obj.order
            #     增加流动资产和总资产
            modify_subjects = ["流动资产合计", "资产总计"]
            if obj["direction_x"] == "借":
                modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
            else:
                modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
        elif obj["subject_type"] == "损益":
            if obj["direction"] == "贷":
                if (next_class == "收入") or (next_class == "成本费用"):
                    this_class = "收入"
                    tb_obj = session.query(TBSubject).filter(TBSubject.order > 600, TBSubject.order < 700).order_by(
                        TBSubject.order.desc()).first()
                    order = tb_obj.order
                    #     增加 一、营业总收入/三、营业利润（亏损以“－”号填列）/四、利润总额（亏损总额以“－”号填列）/五、净利润（净亏损以“－”号填列）/
                    #  九、可供分配的利润/ 十、可供投资者分配的利润/ 十一、未分配利润/未分配利润/归属于母公司股东权益合计/股东权益合计/负债和股东权益总计
                    modify_subjects = ["一、营业总收入", "三、营业利润（亏损以“－”号填列）", "四、利润总额（亏损总额以“－”号填列）",
                                       "五、净利润（净亏损以“－”号填列）", "九、可供分配的利润", "十、可供投资者分配的利润", "十一、未分配利润",
                                       "未分配利润", "归属于母公司股东权益合计", "股东权益合计", "负债和股东权益总计"
                                       ]
                    if obj["direction_x"] == "贷":
                        modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                    else:
                        modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
                else:
                    this_class = "收益"
                    tb_obj = session.query(TBSubject).filter(TBSubject.order > 800, TBSubject.order < 900).order_by(
                        TBSubject.order.desc()).first()
                    order = tb_obj.order
                    #     增加 三、营业利润（亏损以“－”号填列）/四、利润总额（亏损总额以“－”号填列）/五、净利润（净亏损以“－”号填列）/
                    #  九、可供分配的利润/ 十、可供投资者分配的利润/ 十一、未分配利润/未分配利润/归属于母公司股东权益合计/股东权益合计/负债和股东权益总计
                    modify_subjects = ["三、营业利润（亏损以“－”号填列）", "四、利润总额（亏损总额以“－”号填列）",
                                       "五、净利润（净亏损以“－”号填列）", "九、可供分配的利润", "十、可供投资者分配的利润", "十一、未分配利润",
                                       "未分配利润", "归属于母公司股东权益合计", "股东权益合计", "负债和股东权益总计"
                                       ]
                    if obj["direction_x"] == "贷":
                        modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                    else:
                        modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            else:
                this_class = "成本费用"
                tb_obj = session.query(TBSubject).filter(TBSubject.order > 700, TBSubject.order < 800).order_by(
                    TBSubject.order.desc()).first()
                order = tb_obj.order
                #     增加 三、营业利润（亏损以“－”号填列）/四、利润总额（亏损总额以“－”号填列）/五、净利润（净亏损以“－”号填列）/
                #  九、可供分配的利润/ 十、可供投资者分配的利润/ 十一、未分配利润/未分配利润/归属于母公司股东权益合计/股东权益合计/负债和股东权益总计
                modify_subjects = ["三、营业利润（亏损以“－”号填列）", "四、利润总额（亏损总额以“－”号填列）",
                                   "五、净利润（净亏损以“－”号填列）", "九、可供分配的利润", "十、可供投资者分配的利润", "十一、未分配利润",
                                   "未分配利润", "归属于母公司股东权益合计", "股东权益合计", "负债和股东权益总计"
                                   ]
                if obj["direction_x"] == "贷":
                    modify_all_tb(modify_subjects, obj["subject_name"], "+", session)
                else:
                    modify_all_tb(modify_subjects, obj["subject_name"], "-", session)
            first_class = "损益"
        else:
            raise Exception("类型识别错误，请检查类别设置是否正确")

        #  增加类别
        fs_subject = input("{}请输入报表对应的名称{}".format(obj["subject_name"],
                                                   df_std[df_std["second_class"] == this_class]["fs_subject"].unique()))
        subjectcontrast = SubjectContrast(origin_subject=obj["subject_name"], tb_subject=obj['subject_name'],
                                          fs_subject=fs_subject, coefficient=1, direction=obj["direction_x"],
                                          first_class=first_class, second_class=this_class)
        session.add(subjectcontrast)
        tbsubject = TBSubject(show=obj["subject_name"], subject=obj["subject_name"], direction=obj["direction_x"],
                              order=order + 1)
        session.add(tbsubject)
        session.commit()

def append_all_gradation_subjects(df_km, df_xsz):
    '''
    为序时账添加所有级别的会计科目编码和名称
    :param df_km: 科目余额表
    :param df_xsz: 序时账
    :return: 添加过所有级别会计科目编码和名称的序时账
    '''
    # 添加科目编码长度列
    df_km = df_km.copy()
    df_xsz = df_xsz.copy()

    df_km['subject_length'] = df_km['subject_num'].str.len()
    df_km_subject = df_km[['subject_num', 'subject_name']]
    df_km_subject = df_km_subject.rename({'subject_num': 'std_subject_num'}, axis='columns')
    # 获取各科目级次和长度
    df_km_gradation = df_km.drop_duplicates('subject_gradation', keep='first')
    df_km_gradation = df_km_gradation[['subject_gradation', 'subject_length']].sort_values(by="subject_length")
    # 给序时账添加所有的科目级别编码和科目名称
    gradation_subject_and_length = list(zip(df_km_gradation['subject_gradation'], df_km_gradation['subject_length']))
    for i in range(len(gradation_subject_and_length)):
        subject_num_length = gradation_subject_and_length[i][1]
        subject_num_name = 'subject_num_{}'.format(i + 1)
        df_xsz[subject_num_name] = df_xsz['subject_num'].str.slice(0, subject_num_length)
        df_xsz = pd.merge(df_xsz, df_km_subject, how='left', left_on=subject_num_name, right_on="std_subject_num",
                          suffixes=('', '_{}'.format(i + 1)))
        df_xsz = df_xsz.drop(columns=['std_subject_num'])
    return df_xsz

def check_profit_subject_dirction(df_km, df_xsz, engine, add_suggestion,start_time,end_time,session):
    '''
    检查序时账中的损益科目是否核算方向正确，不正确的调整方向
    :param df_km: 科目余额表
    :param df_xsz: 待修改的序时账
    :return: 返回调整后的序时账
    '''
    # 检查是否所有的损益类项目的核算都正确
    # 第一步：获取所有损益类核算项目
    # 第二部：获取所有损益类核算项目的标准方向
    # 第三部：检查是否存在相反方向核算且不属于损益结转的情况
    # 第四步：将核算方向相反的凭证予以调整
    df_xsz_new = df_xsz.copy().set_index(['month', 'vocher_type', 'vocher_num', 'subentry_num'])
    # 第一步：获取所有损益类核算项目
    df_km_first_subject = df_km[df_km['subject_gradation'] == 1]
    df_km_first_subject_profit = df_km_first_subject[df_km_first_subject["subject_num"].str.startswith('6')]
    df_km_first_subject_profit = df_km_first_subject_profit[['subject_num', 'subject_name']]
    # 第二部：获取所有损益类核算项目的标准方向
    df_std = pd.read_sql_table('subjectcontrast', engine)
    df_km_first_subject_profit_direction = pd.merge(df_km_first_subject_profit, df_std, how="inner",
                                                    left_on='subject_name',
                                                    right_on="origin_subject")
    df_km_first_subject_profit_direction = df_km_first_subject_profit_direction[
        ["subject_num", "subject_name", "direction"]]
    # 所有的损益类凭证
    df_xsz_profit = df_xsz[df_xsz['subject_name_1'].isin(df_km_first_subject_profit_direction['subject_name'])]
    # 合并损益类凭证列表和损益类核算项目的标准方向
    df_xsz_profit = pd.merge(df_xsz_profit, df_km_first_subject_profit_direction, how="left", left_on="subject_name_1",
                             right_on="subject_name", suffixes=('_x', ''))
    # 获取核算相反的凭证
    df_xsz_profit_reverse = df_xsz_profit[((df_xsz_profit["direction"] == "借") & (df_xsz_profit["credit"].abs() > 1e-5)) |
                                          ((df_xsz_profit["direction"] == "贷") & (df_xsz_profit["debit"].abs() > 1e-5))]
    df_xsz_profit_reverse_record = df_xsz_profit_reverse[["month", "vocher_num", "vocher_type"]].drop_duplicates()
    # 获取相反凭证的记录
    reverse_records = df_xsz_profit_reverse_record.to_dict('records')
    # 获取相反凭证的完整借贷方
    df_xsz_profit_reverse = pd.merge(df_xsz, df_xsz_profit_reverse_record, how="inner",
                                     on=["month", "vocher_num", "vocher_type"])
    # 第三部：检查是否存在相反方向核算且不属于损益结转的情况
    # 检查每一笔相反凭证中是否包含本年利润，如果包含则是正常的结转损益，不用理会
    for record in reverse_records:
        df_tmp = df_xsz_profit_reverse[(df_xsz_profit_reverse["month"] == record["month"])
                                       & (df_xsz_profit_reverse["vocher_num"] == record["vocher_num"])
                                       & (df_xsz_profit_reverse["vocher_type"] == record["vocher_type"])
                                       ]
        # 检查凭证中是否包含本年利润，如果不包含则调整序时账
        if (not df_tmp["subject_name_1"].str.contains('本年利润', regex=False).any()) and (not df_tmp["subject_name_1"].str.contains('利润分配', regex=False).any()):
            # 第四部：修改序时账
            # 合并标准方向
            df_tmp = pd.merge(df_tmp, df_km_first_subject_profit_direction, left_on="subject_num_1",
                              right_on="subject_num", how="left", suffixes=("", "_y"))
            for obj in gen_df_line(df_tmp):
                if obj['direction'] == "借" and abs(obj['credit']) > 1e-5:
                    # 借贷方金额互换
                    tmp = df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'credit']
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'debit'] = -tmp
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'credit'] = 0.00

                    tmp1 = df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'credit_foreign_currency']
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'debit_foreign_currency'] = -tmp1
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'credit_foreign_currency'] = 0.00
                    #    提建议
                    add_suggestion(kind="会计处理",
                                   content="{}年{}月{}-{}号凭证损益类项目记账不符合规范，建议收入类科目发生时计入贷方，费用类项目发生时计入借方".format(
                                       obj['year'], obj['month'], obj['vocher_type'], obj['vocher_num']),
                                   start_time=start_time,
                                   end_time=end_time,
                                   session=session
                                   )
                elif obj['direction'] == "贷" and abs(obj['debit']) > 1e-5:
                    # 借贷方金额互换
                    tmp = df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'debit']
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'credit'] = -tmp
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'], obj['subentry_num']), 'debit'] = 0.00
                    tmp1 = df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'debit_foreign_currency']
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'credit_foreign_currency'] = -tmp1
                    df_xsz_new.loc[
                        (obj['month'], obj['vocher_type'], obj['vocher_num'],
                         obj['subentry_num']), 'debit_foreign_currency'] = 0.00
                    #    提建议
                    add_suggestion(kind="会计处理",
                                   content="{}年{}月{}-{}号凭证损益类项目记账不符合规范，建议收入类科目发生时计入贷方，费用类项目发生时计入借方".format(
                                       obj['year'], obj['month'], obj['vocher_type'], obj['vocher_num']),
                                   start_time=start_time,
                                   end_time=end_time,
                                   session=session
                                   )
    df_xsz_new = df_xsz_new.reset_index()
    return df_xsz_new

def recaculate_km(df_km, df_xsz,type):
    '''
    将利润分配，本年利润和损益表的期初数全部调整为利润分配。
    :param df_km: 科目余额表
    :param df_xsz: 序时账
    :param type: TB类型，未审TB,调整数TB和审定数TB,unAudited,adjustment,audited
    :return: 新的科目余额表
    '''
    # 获取科目余额表期初数
    if type=="unAudited" or type=="audited":
        df_km_new = df_km[
            ["id", "start_time", "end_time", "subject_num", "subject_name",
             "subject_type", "direction", "is_specific", "subject_gradation","initial_amount"
             ]
        ].copy()
    elif type == "adjustment":
        df_km_new = df_km[
            ["id", "start_time", "end_time", "subject_num", "subject_name",
             "subject_type", "direction", "is_specific", "subject_gradation"
             ]
        ].copy()
        df_km_new['initial_amount'] = 0.00
    else:
        raise Exception("tb类型错误")

    df_km_new["origin_initial"] = df_km["initial_amount"]
    df_km_new["origin_debit"] = df_km["debit_amount"]
    df_km_new["origin_credit"] = df_km["credit_amount"]
    df_km_new["origin_terminal"] = df_km["terminal_amount"]
    df_km_new['debit_amount'] = 0.00
    df_km_new['credit_amount'] = 0.00
    df_km_new['terminal_amount'] = 0.00
    df_km_new = df_km_new.set_index('subject_num')
    profit_dividend_subject_num = get_subject_num_by_name("利润分配",df_km)

    if len(df_xsz)>0:
        # 计算序时账发生额
        df_xsz_pivot = df_xsz.pivot_table(values=['debit', 'credit'], index='subject_num', aggfunc='sum')
        # 重新计算科目余额表
        # 重算期初数
        # 首先计算年初未分配利润
        initial_credit = df_km_new[df_km_new.index.str.startswith("6") &
                                   (df_km_new["direction"] == "贷") &
                                   (df_km_new["is_specific"])]["initial_amount"].sum()
        initial_debit = df_km_new[df_km_new.index.str.startswith("6")&
                                  (df_km_new["direction"] == "借") &
                                  (df_km_new["is_specific"])]["initial_amount"].sum()
        profit_dividend = df_km_new[(df_km_new["subject_name"]=="利润分配") & (df_km_new["subject_gradation"]==1)]["initial_amount"].sum()
        profit_this_year = df_km_new[(df_km_new["subject_name"]=="本年利润") & (df_km_new["subject_gradation"]==1)]["initial_amount"].sum()
        # 确定利润分配期初数=本年利润+利润分配+损益类科目期初数
        df_km_new.at[profit_dividend_subject_num, "initial_amount"] = profit_dividend + profit_this_year + initial_credit - initial_debit

        # 确定借方发生额/贷方发生额，损益类科目结转分录中应该减去期初自动结转的部分。
        for i in range(len(df_km_new)):
            subject_num = df_km_new.index[i]
            # 序时账透视表中筛选出所有科目和子科目
            df_xsz_pivot_tmp = df_xsz_pivot.loc[df_xsz_pivot.index.str.startswith(subject_num)]
            # 期初数
            initial_amount = df_km_new.at[subject_num, "origin_initial"]
            # 序时账借方合计
            debit = df_xsz_pivot_tmp['debit'].sum()
            # 序时账贷方合计
            credit = df_xsz_pivot_tmp['credit'].sum()
            # 因为上面利润分配期初数确认时将本年利润和损益类科目的期初数结转了一次，在本年度做一次冲销处理。将损益类科目的期初数从本年结转发生额中减去，
            if (str(subject_num).startswith("6") and abs(initial_amount)>1e-5) or (
                    df_km_new.at[subject_num, "subject_name"] == "本年利润" and abs(initial_amount) > 1e-5) :
                if df_km_new.at[subject_num, "direction"] == "借":
                    df_km_new.at[subject_num, "debit_amount"] = debit
                    df_km_new.at[subject_num, "credit_amount"] = credit - initial_amount
                    df_km_new.at[subject_num, "initial_amount"] = 0.00
                    df_km_new.at[subject_num, "terminal_amount"] = df_km_new.at[subject_num, "initial_amount"] + df_km_new.at[subject_num, "debit_amount"] - df_km_new.at[subject_num, "credit_amount"]
                elif df_km_new.at[subject_num, "direction"] == "贷":
                    df_km_new.at[subject_num, "debit_amount"] = debit - initial_amount
                    df_km_new.at[subject_num, "credit_amount"] = credit
                    df_km_new.at[subject_num, "initial_amount"] = 0.00
                    df_km_new.at[subject_num, "terminal_amount"] = df_km_new.at[subject_num, "initial_amount"] - df_km_new.at[subject_num, "debit_amount"] + df_km_new.at[subject_num, "credit_amount"]
            else:
                df_km_new.at[subject_num, "debit_amount"] = debit
                df_km_new.at[subject_num, "credit_amount"] = credit
                if df_km_new.at[subject_num, "direction"] == "借":
                    df_km_new.at[subject_num, "terminal_amount"] = df_km_new.at[
                                                                        subject_num, "initial_amount"] + debit - credit
                elif df_km_new.at[subject_num, "direction"] == "贷":
                    df_km_new.at[subject_num, "terminal_amount"] = df_km_new.at[
                                                                        subject_num, "initial_amount"] - debit + credit
        # 检查期末数中的损益是否有数据，如有做一次结转处理。自动结转未结转损益。
            if (str(subject_num).startswith("6") and abs(df_km_new.at[subject_num, "terminal_amount"])>1e-5) :
                modify_amount = df_km_new.at[subject_num, "terminal_amount"]
                if df_km_new.at[subject_num, "direction"] == "借":
                    df_km_new.at[subject_num, "credit_amount"] = df_km_new.at[subject_num, "credit_amount"] + modify_amount
                    df_km_new.at[subject_num, "terminal_amount"] = 0.00
                #     同时修改利润分配
                    df_km_new.at[profit_dividend_subject_num, "debit_amount"] = df_km_new.at[profit_dividend_subject_num, "debit_amount"] + modify_amount
                    df_km_new.at[profit_dividend_subject_num, "terminal_amount"] = df_km_new.at[profit_dividend_subject_num, "terminal_amount"] - modify_amount
                elif df_km_new.at[subject_num, "direction"] == "贷":
                    df_km_new.at[subject_num, "debit_amount"] = df_km_new.at[subject_num, "debit_amount"] + modify_amount
                    df_km_new.at[subject_num, "terminal_amount"] = 0.00
                    #     同时修改利润分配
                    df_km_new.at[profit_dividend_subject_num, "credit_amount"] = df_km_new.at[
                                                                                    profit_dividend_subject_num, "credit_amount"] + modify_amount
                    df_km_new.at[profit_dividend_subject_num, "terminal_amount"] = df_km_new.at[
                                                                                       profit_dividend_subject_num, "terminal_amount"] + modify_amount
    df_km_new = df_km_new.reset_index()
    return df_km_new

def get_bad_debt_value_and_origin(df_one_line):
    if df_one_line["direction"].values[0] == "借":
        # 获取应收账款坏账准备金额
        value = -df_one_line["terminal_amount"].values[0]
    else:
        # 获取应收账款坏账准备金额
        value = df_one_line["terminal_amount"].values[0]
    return value,""

def get_bad_debt(df_km, add_suggestion,start_time,end_time):
    '''
    bad debts in accounts receivable
    获取应收账款坏账准备和其他应收款坏账准备期末数
    :return: (应收账款坏账准备，其他应收款坏账准备)
    '''

    # 获取坏账准备期末金额，如果等于0，则应收账款坏账准备和其他应收款坏账准备都为0
    bad_debt_ar = 0.00
    bad_debt_or = 0.00

    bad_debt = get_subject_value_by_name("坏账准备", df_km, "terminal_amount")
    bad_debt_df = df_km[df_km["subject_name"]=="坏账准备"]
    if math.isclose(bad_debt, 0.00, rel_tol=1e-5):
        return bad_debt_ar,bad_debt_or
    else:
        # 获取坏账准备明细科目，分别分析应收账款坏账准备和其他应收款坏账准备
        df_km_bad_debt = get_detail_subject_df("坏账准备", df_km)
        if len(df_km_bad_debt) > 0:
            # 应收账款坏账准备
            df_km_bad_debt_ar = df_km_bad_debt[(df_km_bad_debt["subject_name"].str.contains("应收")) & (
                ~df_km_bad_debt["subject_name"].str.contains("其他"))]
            # 其他应收款坏账准备
            df_km_bad_debt_or = df_km_bad_debt[df_km_bad_debt["subject_name"].str.contains("其他应收")]
            if len(df_km_bad_debt_ar) == 1:
                value,origin = get_bad_debt_value_and_origin(df_km_bad_debt_ar)
                bad_debt_ar = value
            if len(df_km_bad_debt_or) == 1:
                value, origin = get_bad_debt_value_and_origin(df_km_bad_debt_or)
                bad_debt_or = value
            if bad_debt_ar + bad_debt_or == bad_debt:
                return bad_debt_ar, bad_debt_or
            else:
                value, origin = get_bad_debt_value_and_origin(bad_debt_df)
                bad_debt_ar = value
                return bad_debt_ar, bad_debt_or
        else:
            add_suggestion(
                kind="会计处理",
                content="建议在坏账准备科目下设“应收账款坏账准备”和“其他应收款坏账准备”两个科目",
                start_time=start_time,
                end_time=end_time,
            )
            value, origin = get_bad_debt_value_and_origin(bad_debt_df)
            bad_debt_ar = value
            return bad_debt_ar, bad_debt_or

def get_df_km_occurrence_value_and_origin(df_one_line,direction):
    if direction == "借":
        value = df_one_line["debit_amount"].values[0]
    else:
        value = df_one_line["credit_amount"].values[0]
    return value,""

def get_reserve_fund_provision(df_km, add_suggestion,start_time,end_time):
    '''
    获取本期计提的盈余公积
    :param df_km:科目余额表
    :return:本期计提的各盈余公积明细
    '''
    # 法定盈余公积
    legal_reserve = 0.00
    # 任意盈余公积
    discretionary_surplus_reserve = 0.00
    # 法定公益金
    legal_public_welfare_fund = 0.00
    # 储备基金
    reserve_fund = 0.00
    # 企业发展基金
    enterprise_development_fund = 0.00
    # 利润归还投资
    profit_return_investment = 0.00

    match_table = {
        "法定盈余公积": legal_reserve,
        "任意盈余公积": discretionary_surplus_reserve,
        "法定公益金": legal_public_welfare_fund,
        "储备基金": reserve_fund,
        "企业发展基金": enterprise_development_fund,
        "利润归还投资": profit_return_investment
    }

    df_reserve_fund = df_km[df_km["subject_name"] == "盈余公积"]
    # 如果公司没有设置盈余公积科目,或者盈余公积科目借方发生额和贷方发生额都是0
    if (len(df_reserve_fund) == 0) or \
            (len(df_reserve_fund) == 1 and
             (math.isclose(get_subject_value_by_name("盈余公积", df_km, "credit_amount"), 0.0, rel_tol=1e-5)) and
             (math.isclose(get_subject_value_by_name("盈余公积", df_km, "debit_amount"), 0.0, rel_tol=1e-5))
            ):
        return legal_reserve, discretionary_surplus_reserve, legal_public_welfare_fund, reserve_fund, enterprise_development_fund, profit_return_investment

    df_reserve_fund_detail = get_detail_subject_df("盈余公积", df_km)
    # 如果设置了盈余公积，检查有没有明细科目
    if len(df_reserve_fund_detail) == 0:
        # 如果盈余公积没有明细核算，检查利润分配是否有明细核算，根据利润分配来确认各个明细
        if df_reserve_fund["terminal_amount"].values[0] > 1e-5:
            add_suggestion(kind="会计处理",
                           content="盈余公积账户下应当分别设“法定盈余公积”“任意盈余公积”“法定公益金”“储备基金”“企业发展基金”和“利润归还投资”等进行明细核算",
                           start_time=start_time,
                           end_time=end_time,
                           )
        # 通过利润分配确认盈余公积明细表
        df_profit_distribution_detail = get_detail_subject_df("利润分配", df_km)
        if len(df_profit_distribution_detail) == 0:
            value,origin = get_df_km_occurrence_value_and_origin(df_reserve_fund,"贷")
            legal_reserve  = value
            return legal_reserve, discretionary_surplus_reserve, legal_public_welfare_fund, reserve_fund, enterprise_development_fund, profit_return_investment
        else:
            for obj in gen_df_line(df_profit_distribution_detail):
                # 获取数据源
                value = obj["debit_amount"]
                for name in match_table:
                    if name in obj["subject_name"]:
                        match_table[name] = value
    else:
        for obj in gen_df_line(df_reserve_fund_detail):
            value = obj["credit_amount"]
            for name in match_table:
                if name in obj["subject_name"]:
                    match_table[name] = value
    return legal_reserve, discretionary_surplus_reserve, legal_public_welfare_fund, reserve_fund, enterprise_development_fund, profit_return_investment

def get_none_adjust_xsz(df_xsz):
    '''
    将序时账中的调整分录摘出来，只剩下非调整分录
    :param df_xsz:
    :return:
    '''
    df_xsz_record = df_xsz[
        ["month", "vocher_num", "vocher_type"]].drop_duplicates()
    records = df_xsz_record.to_dict('records')
    none_adjust_dfs = []
    for record in records:
        df_tmp = df_xsz[(df_xsz["month"] == record["month"])
                                & (df_xsz["vocher_num"] == record["vocher_num"])
                                & (df_xsz["vocher_type"] == record["vocher_type"])
                                ]
        contain_audit_str_df = df_tmp[df_tmp["description"].str.contains("审计")]
        contain_adjust_str_df = df_tmp[df_tmp["description"].str.contains("调整")]
        if len(contain_audit_str_df) > 0 or len(contain_adjust_str_df) > 0 :
            pass
        else:
            none_adjust_dfs.append(df_tmp)
    if len(none_adjust_dfs) > 0:
        df_xsz_new = pd.concat(none_adjust_dfs)
    else:
        df_xsz_new = df_xsz[df_xsz["subject_name"] == ""]
    return df_xsz_new

def get_profit_distribution(df_km, df_xsz, add_suggestion,start_time,end_time,session,engine):
    '''
    分析利润分配科目
    :param df_km:
    :param df_xsz:
    :return:
    '''
    # 获取标准科目对照表
    df_std = pd.read_sql_table('subjectcontrast', engine)
    # 转作资本（或股本）的普通股股利
    convert_to_capital = 0.00
    # 优先股股利
    preferred_dividend = 0.00
    # 普通股股利
    dividend = 0.00
    # 年初未分配利润调整：包括通过以前年度损益调整科目的调整、未通过以前年度损益调整科目直接计入本年利润或者利润分配科目
    adjustment_profit = 0.00
    # 盈余公积
    legal_reserve, discretionary_surplus_reserve, legal_public_welfare_fund, reserve_fund, enterprise_development_fund, profit_return_investment = get_reserve_fund_provision(
        df_km, add_suggestion,start_time,end_time)
    match_table = {
        "法定盈余公积": legal_reserve,
        "任意盈余公积": discretionary_surplus_reserve,
        "法定公益金": legal_public_welfare_fund,
        "储备基金": reserve_fund,
        "企业发展基金": enterprise_development_fund,
        "利润归还投资": profit_return_investment
    }
    #     检查利润分配是否有明细科目
    df_profit_distribution_detail = get_detail_subject_df("利润分配", df_km)
    # 利润分配没有设置明细科目
    if len(df_profit_distribution_detail) == 0:
        add_suggestion(kind="会计处理",
                       content="利润分配账户下应当分别设“提取法定盈余公积”“提取任意盈余公积”“应付现金股利(或利润)”“转作股本的股利”“盈余公积补亏”和“未分配利润”等进行明细核算",
                       start_time=start_time,
                       end_time=end_time,
                       session=session
                       )
    # 分析序时账分别填列
    # 获取利润分配的所有明细账
    # 获取利润分配的科目编码
    subject_num_profit = get_subject_num_by_name("利润分配", df_km)
    # 获取利润分配的所有凭证包含借贷方
    if subject_num_profit:
        df_profit_xsz = get_xsz_by_subject_num(df_xsz, grade=1, subject_num=subject_num_profit)
        df_this_year_profit_xsz = df_profit_xsz[df_profit_xsz["subject_name_1"]=="本年利润"]
        # 从利润分配凭证中减去本年利润结转类凭证
        for obj in gen_df_line(df_this_year_profit_xsz):
            df_profit_xsz = df_profit_xsz[~((df_profit_xsz["month"] == obj["month"]) & (df_profit_xsz["vocher_num"] == obj["vocher_num"]) & (
                    df_profit_xsz["vocher_type"] == obj["vocher_type"]))]
        # 检查利润分配-提取盈余公积
        # 获取利润分配凭证中的提取盈余公积的凭证
        subject_num_reserve = get_subject_num_by_name("盈余公积", df_km)
        df_xsz_reserve = pd.DataFrame()
        if subject_num_reserve:
            df_xsz_reserve = get_xsz_by_subject_num(df_profit_xsz, grade=1, subject_num=subject_num_reserve)
        #     # 检查序时账提取盈余公积与科目余额表是否一致
            df_profit_xsz_reserve = df_xsz_reserve[df_xsz_reserve["subject_name_1"] == "利润分配"]
            reserve_value_in_xsz = df_profit_xsz_reserve["debit"].sum() - df_profit_xsz_reserve["credit"].sum()
            reserves_sum = legal_reserve+discretionary_surplus_reserve+legal_public_welfare_fund+reserve_fund+enterprise_development_fund+profit_return_investment
            if abs(reserve_value_in_xsz - reserves_sum) > 1e-5:
                # 根据序时账计算盈余公积
                # 将序时账中的调整分录扣除
                df_xsz_reserve = get_none_adjust_xsz(df_xsz_reserve)
                # 计算盈余公积的各项值
                for name in match_table:
                    df_reserve = df_xsz_reserve[df_xsz_reserve["subject_name"] == name]
                    match_table[name] = df_reserve["credit"].sum() - df_reserve["debit"].sum()

        # 检查利润分配-转为资本
        subject_num_paid_up_capital = get_subject_num_by_similar_name("实收资本", df_km)
        if not subject_num_paid_up_capital:
            subject_num_paid_up_capital = get_subject_num_by_similar_name("股本", df_km)
        subject_num_captial_reserve = get_subject_num_by_name("资本公积", df_km)
        subject_num_capital = []
        for item in [subject_num_paid_up_capital, subject_num_captial_reserve]:
            if item:
                subject_num_capital.append(item)
        df_xsz_capital = get_xsz_by_subject_num(df_profit_xsz, grade=1, subject_num=subject_num_capital)
        # 扣除调整分录
        df_xsz_capital = get_none_adjust_xsz(df_xsz_capital)
        df_profit_xsz_capital = df_xsz_capital[df_xsz_capital["subject_name_1"] == "利润分配"]
        value = df_profit_xsz_capital["debit"].sum() - df_profit_xsz_capital["credit"].sum()
        convert_to_capital = value

        # 分配股利
        subject_num_ividend_payable = get_subject_num_by_name("应付股利", df_km)
        subject_num_cash1 = get_subject_num_by_name("现金", df_km)
        subject_num_cash2 = get_subject_num_by_name("库存现金", df_km)
        subject_num_bank_deposit = get_subject_num_by_name("银行存款", df_km)
        subject_num_dividend = []
        for item in [subject_num_ividend_payable, subject_num_cash1, subject_num_cash2, subject_num_bank_deposit]:
            if item:
                subject_num_dividend.append(item)
        df_xsz_dividend = get_xsz_by_subject_num(df_profit_xsz, grade=1, subject_num=subject_num_dividend)
        # 扣除调整分录
        df_xsz_dividend = get_none_adjust_xsz(df_xsz_dividend)
        #     优先股股利
        df_preferred_dividend = df_xsz_dividend[
            (df_xsz_dividend["subject_name_1"] == "利润分配") &
            (df_xsz_dividend["subject_name_2"].str.contains("优先股"))]
        if len(df_preferred_dividend)>0:
            value = df_preferred_dividend["debit"].sum() - df_preferred_dividend["credit"].sum()
            preferred_dividend = value
        #     普通股股利
        df_profit_xsz_dividend = df_xsz_dividend[(df_xsz_dividend["subject_name_1"] == "利润分配") &
            ~(df_xsz_dividend["subject_name_2"].str.contains("优先股"))
        ]
        if len(df_profit_xsz_dividend)>0:
            value = df_profit_xsz_dividend["debit"].sum() - df_profit_xsz_dividend["credit"].sum()
            dividend = value

        # 利润调整1--以前年度损益调整
        subject_num_prior_year_income_adjustment = get_subject_num_by_name("以前年度损益调整", df_km)
        df_xsz_adjustment = pd.DataFrame()
        if subject_num_prior_year_income_adjustment:
            df_xsz_adjustment = get_xsz_by_subject_num(df_profit_xsz, grade=1,
                                                       subject_num=subject_num_prior_year_income_adjustment)
        df_profit_xsz_adjustment = df_xsz_adjustment[df_xsz_adjustment["subject_name_1"] == "以前年度损益调整"]
        # 利润调整2--未通过损益表项目直接计入本年利润
        df_none_profit_and_loss_xsz = get_not_through_profit_and_loss_to_this_year_profit(df_km,df_xsz,start_time,end_time,add_suggestion,session)

        # 本年利润
        subject_num_this_year_profit = get_subject_num_by_name("本年利润", df_km)
        df_xsz_this_year_profit = pd.DataFrame()
        if subject_num_this_year_profit:
            df_xsz_this_year_profit = get_xsz_by_subject_num(df_profit_xsz, grade=1,
                                                             subject_num=subject_num_this_year_profit)
        df_has_check = pd.concat(
            [df_xsz_this_year_profit, df_xsz_adjustment, df_xsz_dividend, df_xsz_capital, df_xsz_reserve])
        df_has_check = df_has_check[["month", "vocher_num", "vocher_type"]].drop_duplicates()

        df_tmp = df_profit_xsz.copy()
        # 获取未检查的可能的调整分录
        for obj in gen_df_line(df_has_check):
            df_tmp = df_tmp[~((df_tmp["month"] == obj["month"]) & (df_tmp["vocher_num"] == obj["vocher_num"]) & (
                        df_tmp["vocher_type"] == obj["vocher_type"]))]
        # 利润调整3- -直接计入利润分配科目
        df_rest_profit = pd.DataFrame()
        if len(df_tmp) > 0:
            # 扣除掉损益结转类科目
            # （1）如果含有非损益类科目，则不是损益结转凭证
            # （2）如果不含有非损益类科目，但损益类科目方向不相反（费用类为借方，收入类为贷方，则认定为调整分录）
            profit_and_loss = df_tmp[df_tmp["subject_num"].str.startswith("6")]
            profit_and_loss = pd.merge(profit_and_loss, df_std, how="inner",
                                                            left_on='subject_name_1',
                                                            right_on="origin_subject")
            for obj in gen_df_line(profit_and_loss):
                if (obj["direction"] == "借" and abs(obj["credit"])>0) or  (obj["direction"] == "贷" and abs(obj["debit"])>0):
                    df_tmp = df_tmp[~((df_tmp["month"] == obj["month"]) & (df_tmp["vocher_num"] == obj["vocher_num"]) & (
                            df_tmp["vocher_type"] == obj["vocher_type"]))]
            df_rest_profit = df_tmp[df_tmp["subject_name_1"] != "利润分配"]
            add_suggestion(
                kind="会计处理",
                content="涉及到以前年度损益调整项目通过“以前年度损益调整”科目核算后再转入利润分配科目。",
                start_time=start_time,
                end_time=end_time,
                session=session
            )
        df_profit_and_other_xsz_adjustment = pd.concat([df_rest_profit,df_profit_xsz_adjustment,df_none_profit_and_loss_xsz])
        adjustment_profit = df_profit_and_other_xsz_adjustment["debit"].sum() - df_profit_and_other_xsz_adjustment["credit"].sum()
    else:
        raise Exception("公司没有设置利润分配科目")

    result = [convert_to_capital, preferred_dividend, dividend, adjustment_profit, *list(match_table.values())]
    return tuple(result)

def get_not_through_profit_and_loss_to_this_year_profit(df_km,df_xsz,start_time,end_time,add_suggestion,session):
    '''
    计算直接计入本年利润的资产负债项目调整。
    :param df_km:
    :param df_xsz:
    :param start_time:
    :param end_time:
    :param session:
    :return:
    '''
    subject_num_this_year_profit = get_subject_num_by_name("本年利润", df_km)
    if subject_num_this_year_profit:
        df_xsz_this_year_profit = get_xsz_by_subject_num(df_xsz, grade=1,
                                                         subject_num=subject_num_this_year_profit)
        df_none_profit_and_loss_xsz = df_xsz_this_year_profit[~(df_xsz_this_year_profit["subject_num"].str.contains("6"))&
                                                               (df_xsz_this_year_profit["subject_name_1"] != "本年利润")&
                                                           (df_xsz_this_year_profit["subject_name_1"] != "利润分配")]


        if len(df_none_profit_and_loss_xsz) > 0:

            add_suggestion(
                kind="会计处理",
                content="涉及到损益类科目核算应通过利润表科目再转入“本年利润”,不应直接计入本年利润。",
                start_time=start_time,
                end_time=end_time,
                session=session
            )
            return df_none_profit_and_loss_xsz
    return pd.DataFrame()


def parse_df_tb_subject_formula(df_tb, subject):
    '''
    解析TBsubject中的公式，按照公式计算出值
    :param df_tb:
    :param subject:
    :return:
    '''
    formula = subject.split("%")
    formula_items = formula[1:len(formula) - 1]
    formula_str = ""
    for item in formula_items:
        if item in ["+", "-", "*", "/"]:
            formula_str = formula_str + item
        else:
            value = df_tb.at[item, "amount"]
            formula_str = formula_str + "{}".format(value)
    return eval(formula_str)

def get_tb(df_km, df_xsz, engine, add_suggestion,start_time,end_time,session):
    '''
    根据科目余额表和序时账填写TB
    :param df_km: 科目余额表
    :param df_xsz: 序时账
    :param type: TB类型，未审TB,调整数TB和审定数TB,unAudited,adjustment,audited
    :param engine: 数据库engine
    :param add_suggestion: 提建议
    :return: tb
    '''
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df_km = df_km.copy()
    df_xsz = df_xsz.copy()
    # 标准科目对照表和标准tb科目表,准备空白TB
    df_subject_contrast = pd.read_sql_table('subjectcontrast', engine)
    df_tb_subject = pd.read_sql_table('tbsubject', engine)
    df_tb_subject['amount'] = 0.00
    df_tb_subject["origin"] = ""
    df_tb = df_tb_subject.set_index("subject")
    # 由于TB中不包含坏账准备/本年利润/利润分配/以前年度损益调整四个科目，对于这四个科目的填报需要单独分析后填列
    # 坏账准备应分为应收账款坏账准备和其他应收款坏账准备
    # 利润分配应该按照途径来填写不同的分配途径
    # 利润分配/本年利润/以前年度损益调整科目分析以填制年初未分配利润
    # 获取坏账准备明细，包括应收账款坏账准备和其他应收款坏账准备
    bad_debt_ar, bad_debt_or = get_bad_debt(df_km, add_suggestion,start_time,end_time)
    # 获取利润分配项目
    convert_to_capital, preferred_dividend, dividend, adjustment_profit, legal_reserve, discretionary_surplus_reserve, legal_public_welfare_fund, reserve_fund, enterprise_development_fund, profit_return_investment = get_profit_distribution(
        df_km, df_xsz, add_suggestion,start_time,end_time,session,engine)
    subject_match = {
        "坏账准备--应收账款": bad_debt_ar,
        "坏账准备--其他应收款": bad_debt_or,
        "利润分配--转作资本的普通股股利": convert_to_capital,
        "利润分配--应付优先股股利": preferred_dividend,
        "利润分配--应付普通股股利": dividend,
        "利润分配--提取法定盈余公积": legal_reserve,
        "利润分配--提取任意盈余公积": discretionary_surplus_reserve,
        "利润分配--提取法定公益金": legal_public_welfare_fund,
        "利润分配--提取储备基金": reserve_fund,
        "利润分配--提取企业发展基金": enterprise_development_fund,
        "利润分配--利润归还投资": profit_return_investment
    }
    # 合并科目余额表和科目对照表
    df_km_first_subject = get_not_null_df_km(df_km, 1)
    df_km_first_subject_not_match = df_km_first_subject[
        ~df_km_first_subject['subject_name'].isin(df_subject_contrast['origin_subject'])]
    df_km_first_subject_not_match = df_km_first_subject_not_match.set_index("subject_name")

    df_km_first_subject_match = pd.merge(df_km_first_subject, df_subject_contrast, left_on="subject_name",
                                         right_on="origin_subject", how="inner")
    df_km_first_subject_match = df_km_first_subject_match.set_index('tb_subject')

    # 遍历TB项目
    for subject in df_tb.index:
        # 如果subject为空则continue
        if not subject:
            continue
        # 如果tb项目在科目余额表中，直接取数
        elif subject in df_km_first_subject_match.index:
            subject_num = str(df_km_first_subject_match.at[subject, 'subject_num'])
            # 如果是资产负债表项目，并且科目余额表方向和TB科目方向一致，则直接取期末数
            location = {"subject_num": subject_num, "subject_name": subject}
            if not subject_num.startswith('6'):
                # 判断科目方向是否一致
                if df_km_first_subject_match.at[subject, 'direction_x'] == df_km_first_subject_match.at[
                    subject, 'direction_y']:
                    # 添加数据源
                    df_tb.at[subject,"origin"] = ""
                    # 添加数据结果
                    df_tb.at[subject, "amount"] = df_km_first_subject_match.at[subject, 'terminal_amount']
                else:
                    # 添加数据源
                    df_tb.at[subject, "origin"] = ""
                    # 添加数据结果
                    df_tb.at[subject, "amount"] = -df_km_first_subject_match.at[subject, 'terminal_amount']
            else:
                # 如果是利润表项目，则取发生额
                if df_tb.at[subject,"direction"] == "借":
                    # 添加数据源
                    df_tb.at[subject, "origin"] = ""
                    # 添加数据结果
                    df_tb.at[subject, "amount"] = df_km_first_subject_match.at[subject, 'debit_amount']
                else:
                    # 添加数据源
                    df_tb.at[subject, "origin"] = ""
                    # 添加数据结果
                    df_tb.at[subject, "amount"] = df_km_first_subject_match.at[subject, 'credit_amount']
        elif subject in subject_match:
            df_tb.at[subject, "amount"] = subject_match[subject]
            df_tb.at[subject, "origin"] = ""
        elif subject == "年初未分配利润":
            # 利润分配+本年利润+损益类科目贷方-损益类科目借方+年初调整数
            df_tb.at[subject, "origin"] = ""
            if "利润分配" in df_km_first_subject_not_match.index:
                df_tb.at[subject, "amount"] = df_km_first_subject_not_match.at["利润分配", 'initial_amount'] + adjustment_profit
            else:
                df_tb.at[subject, "amount"] = 0.00 + adjustment_profit


    # 最后计算公式
    # 如果是公式的话，则按照公式进行匹配
    for subject in df_tb.index:
        if not subject:
            continue
        if subject.startswith("%"):
            df_tb.at[subject, "amount"] = parse_df_tb_subject_formula(df_tb, subject)
    # 检查TB是否已经平了
    total_assets = df_tb[df_tb["show"].str.strip() == "资产总计"]["amount"].values[0]
    liabilities_and_shareholders_equity = df_tb[df_tb["show"].str.strip() == "负债和股东权益总计"]["amount"].values[0]
    df_tb = df_tb.sort_values(by="order")
    if math.isclose(total_assets, liabilities_and_shareholders_equity, rel_tol=1e-5):
        return df_tb
    else:
        return df_tb


def get_new_km_xsz_df(start_time, end_time,type, engine, add_suggestion, session):
    '''
    获取新的科目余额表和序时账
    :param start_time: 2018-1-1
    :param end_time: 2018-12-31
    :param type: TB类型，未审TB,调整数TB和审定数TB,unAudited,adjustment,audited
    :param engine: 数据库engine
    :param add_suggestion: 添加建议
    :param session: 数据库session
    :return: df_km_new,df_xsz_new
    '''
    # 处理起止时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    check_start_end_date(start_time, end_time)
    year = start_time.year
    start_month = start_time.month
    end_month = end_time.month
    # 从数据库读取科目余额表
    df_km = pd.read_sql_table('subjectbalance', engine)
    df_km = df_km[(df_km['start_time'] == start_time) & (df_km['end_time'] == end_time)]
    # 检查是否存在未识别的一级会计科目
    df_std = pd.read_sql_table('subjectcontrast', engine)
    # 将不存在的一级科目添加到标准对照表和tb中
    add_std_not_exist_subject(df_km, df_std, session)
    # # 获取序时账
    if type=="unAudited":
        df_xsz = pd.read_sql_table('chronologicalaccount', engine)
    elif type == "adjustment":
        df_xsz = pd.read_sql_table('aduitadjustment', engine)
    elif type == "audited":
        df_xsz_origin = pd.read_sql_table('chronologicalaccount', engine)
        df_xsz_adjustment = pd.read_sql_table('aduitadjustment', engine)
        df_xsz = pd.concat([df_xsz_origin, df_xsz_adjustment],ignore_index=True)
    else:
        raise Exception("未识别你要找的tb类型")

    df_xsz = df_xsz[(df_xsz['year'] == year) & (df_xsz['month'] >= start_month) & (df_xsz['month'] <= end_month)]

    # 为序时账添加所有级别的会计科目编码和名称
    df_xsz = append_all_gradation_subjects(df_km, df_xsz)
    # 检查是否所有的损益类项目的核算都正确,不正确则修改序时账
    df_xsz_new = check_profit_subject_dirction(df_km, df_xsz, engine, add_suggestion, start_time, end_time,session)
    # 根据序时账重新计算科目余额表
    df_km_new = recaculate_km(df_km, df_xsz_new,type)
    return df_km_new,df_xsz_new

def recalculation(start_time, end_time,type, engine, add_suggestion, session):
    # 根据序时账和科目余额表重新计算新的科目余额表和序时账，主要是损益核算方向的检查

    df_km_new ,df_xsz_new= get_new_km_xsz_df(start_time, end_time,type, engine, add_suggestion, session)
    # 根据新的科目余额表计算tb
    df_tb = get_tb(df_km_new, df_xsz_new, engine, add_suggestion,start_time, end_time,session)
    df_tb = df_tb.reset_index()
    df_tb = df_tb[["show","amount","order","direction","subject"]]
    tb = df_tb.to_json(orient='records')
    sys.stdout.write(tb)

def save_tb(start_time,end_time,session,df_tb):
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    df_tb = df_tb[['show', 'direction', 'amount']]
    for i in range(len(df_tb)):
        show = df_tb.iat[i, 0]
        direction = df_tb.iat[i, 1]
        amount = df_tb.iat[i, 2]
        tb_item = TB(start_time=start_time,end_time=end_time,subject_name=show,direction=direction,amount=amount,origin="")
        session.add(tb_item)
    session.commit()


if __name__ == '__main__':
    db_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    type = sys.argv[4]
    # db_path = "D:\gewuaduit\db\cjz6d855k0crx07207mls869f-ck12xld4000lq0720pmfai22l.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    from utils import add_suggestion
    # companyname = "深圳市众恒世讯科技股份有限公司"
    # start_time = "2016-1-1"
    # end_time = "2016-12-31"
    # type="unAudited"
    # get_new_km_xsz_df(start_time, end_time,type, engine, add_suggestion, session)
    # recalculation(start_time,end_time,type,engine,add_suggestion,session)


    recalculation(start_time, end_time,type, engine=engine, session=session,add_suggestion=add_suggestion)

