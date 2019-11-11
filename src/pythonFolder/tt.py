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
import pandas as pd



df = pd.read_excel("D:/limin/2016/pz.xlsx", index_col=0)
df.to_excel("D:/limin/2016/pz1.xlsx")