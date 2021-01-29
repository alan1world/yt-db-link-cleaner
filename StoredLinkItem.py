#! /usr/bin/env python
# -*- code: utf-8 -*-

from datetime import datetime

class StoredLinkItem:
    '''Class for storing link data'''
    link_id: int
    raw_link: str
    title: str
    link: str
    source: str
    import_date: str
    real_date: datetime
    original_title: str
    flag_bad_source: bool = False
    flag_bad_title: bool = False
    hash_value: int

    def __init__(
            self, 
            link_id: str,
            raw_link: str,
            title: str,
            link: str,
            source: str,
            import_date: str
        ) -> None:
        self.link_id = link_id
        self.raw_link = raw_link
        self.original_title = title
        self.link = link
        self.source = source
        self.import_date = import_date
        
        self.real_date = datetime.strptime(import_date, '%Y-%m-%d')
        if 'chrome-extension://klbibkeccnjlkjkiokjodocebajanakg' in self.original_title:
            self.title = self.original_title[71:self.original_title.find('&uri=')]
            self.raw_link = f'[{self.title}]({self.link})'
        else:
            self.title = self.original_title
            
        if self.source == 'unknown':
            self.flag_bad_source = True
        if self.title == 'YouTube':
            self.flag_bad_title = True
        
        self.hash_value = hash(self.link)
    
    def __repr__(self) -> str:
        return (f'StoredLinkItem(link_id={self.link_id!r}, raw_link={self.raw_link!r}, '
                f'title={self.title!r}, link={self.link!r}, source={self.source!r}, '
                f'import_date={self.import_date!r})')
    
    def __str__(self) -> str:
        return f'Title: {self.title}, Link: {self.link}, Date: {self.import_date}'
    
    def __hash__(self) -> int:
        return hash(self.link)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.link == other.link
    
    def __ne__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.link != other.link
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.real_date > other.real_date
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.real_date < other.real_date
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.real_date >= other.real_date
    
    def __le__(self, other) -> bool:
        if not isinstance(other, StoredLinkItem):
            return NotImplemented
        return self.real_date <= other.real_date
