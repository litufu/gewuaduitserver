# -*- coding:utf-8 -*-

import sys
from sqlalchemy import create_engine,and_
from sqlalchemy.orm import sessionmaker
from supplier_natrue import add_supplier_nature
from utils import count_time
from entry_classify import analyse_entry
from entry_test import aduit_entry
from check_entry import check_entry
from importance import get_actual_importance_level
from supplier import save_supplier_to_db
from customer import save_customer_to_db

@count_time
def project_init_data(company_type,start_time, end_time, session, engine,add_suggestion):
    '''
    导入数据后的数据初始化
    :param company_type:
    :param start_time:
    :param end_time:
    :param session:
    :param engine:
    :param add_suggestion:
    :return:
    '''
    add_supplier_nature(start_time, end_time, session, engine)
    # # 分析凭证分类
    analyse_entry(start_time, end_time, session, engine, add_suggestion, "yes")
    # # 凭证测试
    aduit_entry(start_time, end_time, session, engine, add_suggestion)
    # 凭证抽查
    actual_importance_level = get_actual_importance_level(company_type, start_time, end_time, engine, session,
                                                          add_suggestion)
    check_entry(start_time, end_time, actual_importance_level, 0.7, 5, 4, "yes", engine, session)
    # 供应商分析
    save_supplier_to_db(engine, session, start_time, end_time)
    # 客户分析
    save_customer_to_db(engine, session, start_time, end_time)


if __name__ == '__main__':
    db_path = sys.argv[1]
    # db_path = "D:\gewuaduit\db\cjz6d8rpd0nat0720w8yj2ave-ck2ok4ozx000i07205dds201w.sqlite"
    engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    company_type = sys.argv[4]
    # start_time="2015-1-1"
    # end_time="2015-12-31"
    # company_type="其他企业"
    from utils import add_suggestion
    project_init_data(company_type, start_time, end_time, session, engine, add_suggestion)
    sys.stdout.write("success")
