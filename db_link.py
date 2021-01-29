#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sqlalchemy

# import Mariadb_activate

# from collections import namedtuple

from sqlalchemy_classes import LinksFinal
from sqlalchemy.orm import sessionmaker

from Mariadb_activate import activate_mariadb

engine = activate_mariadb(check_state=False)
print(engine.table_names())