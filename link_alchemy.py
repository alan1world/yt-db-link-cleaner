#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sqlalchemy
# import mysql.connector as mariadb
# import numpy as np
# import pandas as pd
import Mariadb_activate

from collections import namedtuple
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select

from StoredLinkItem import StoredLinkItem

engine = Mariadb_activate.activate_mariadb()
# engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{usr}:{psswd}@127.0.0.1/{dbase}')
print(engine.table_names())

# Create a MetaData instance
# metadata = MetaData()
# print(metadata.tables)

# reflect db schema to MetaData
# metadata.reflect(bind=engine)
# print(metadata.tables)

# select * from 'links_combined' using select
# conn = engine.connect()

# meta = MetaData(engine).reflect()
# meta = MetaData()
# meta.reflect(bind=engine)
# meta = MetaData(engine)
# meta.reflect()
# print(meta.tables)
# table = meta.tables['final']

# select_st = select([table]).where(
   # table.c.l_name == 'Hello')
# select_st = select([table]).limit(5)
# res = conn.execute(select_st)
# for _row in res:
    # print(_row)
    # print(f'title: {_row[2]}, source: {_row[4]}, date: {_row[5]}')

from sqlalchemy_classes import LinksFinal
from sqlalchemy.orm import sessionmaker

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print("----> order_by(id):")
# query = session.query(User).order_by(User.id)
query = session.query(LinksFinal).order_by(LinksFinal.link_id).limit(5)
for _row in query.all():
    # print(_row.name, _row.fullname, _row.birth)
    print(_row.title, _row.source, _row.importdate)
