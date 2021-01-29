#! /usr/bin/env python
# -*- coding: utf-8 -*-

import keyring, getpass
import mysql.connector as mariadb
import mariadbcontrol

def run_mariadb()->str:
    
    if "Mariadb is not running" in mariadbcontrol.mariadb_is_running():
        mariadbcontrol.mariadb_start()
        print("Mariadb has been started")
        return "stop"
    else:
        print("Mariadb was already running")
        return "leave"
    
def key_implement(dbase:str = 'link_store', usr:str = 'alan', respond:bool=True)->str:
    
    if keyring.get_password(dbase, usr) == None:
        usr_pass = getpass.getpass(prompt="Mysql password:")
        keyring.set_password(dbase, usr, usr_pass)
        if respond:
            print("Password set")
        return usr_pass
    else:
        if respond:
            print("Password found")
        return keyring.get_password(dbase, usr)
    
def activate_mariadb(check_state:bool=True)->object:
    
    import sqlalchemy
    
    usr = 'alan'
    dbase = 'link_store'
    # db='links'
    psswd = key_implement(dbase = dbase, usr = usr, respond=False)
    if check_state:
        # mariadb_state = run_mariadb()
        run_mariadb()
    
    return sqlalchemy.create_engine(f'mysql+mysqlconnector://{usr}:{psswd}@127.0.0.1/{dbase}')
    
# from sqlalchemy import create_engine
# engine = create_engine('mysql+mysqlconnector://[user]:[pw]@127.0.0.1/[dbname]')
# engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{usr}:{psswd}@127.0.0.1/{dbase}', echo=True)
