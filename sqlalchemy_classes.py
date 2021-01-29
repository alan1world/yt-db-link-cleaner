#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# meta = sqlalchemy.MetaData()
Base = declarative_base()

class LinksCombined(Base):
    __tablename__ = 'links_combined'
    
    link_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    raw_link = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    link = sqlalchemy.Column(sqlalchemy.String)
    source = sqlalchemy.Column(sqlalchemy.String)
    importdate = sqlalchemy.Column(sqlalchemy.String)
    
    def __repr__(self):
        return "<LinksCombined(raw_link='%s', title='%s', link='%s', source='%s', importdate='%s')>" % (
            self.raw_link, self.title, self.link,self.source, self.importdate)
    
class LinksFinal(Base):
    __tablename__ = 'final'
    
    link_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    raw_link = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    link = sqlalchemy.Column(sqlalchemy.String)
    source = sqlalchemy.Column(sqlalchemy.String)
    importdate = sqlalchemy.Column(sqlalchemy.String)
    md5check = sqlalchemy.Column(sqlalchemy.String)
    
    def __repr__(self):
        return "<LinksFinal(raw_link='%s', title='%s', link='%s', source='%s', importdate='%s', hash_check='%s')>" % (
            self.raw_link, self.title, self.link,self.source, self.importdate, self.md5check)

class LinksArchive(Base):
    __tablename__ = 'archive'
    
    link_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    raw_link = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    link = sqlalchemy.Column(sqlalchemy.String)
    source = sqlalchemy.Column(sqlalchemy.String)
    importdate = sqlalchemy.Column(sqlalchemy.String)
    
    def __repr__(self):
        return "<LinksArchive(raw_link='%s', title='%s', link='%s', source='%s', importdate='%s')>" % (
            self.raw_link, self.title, self.link,self.source, self.importdate)
