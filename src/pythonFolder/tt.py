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





from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))