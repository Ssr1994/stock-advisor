# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from stockadvisor.settings import DB, SEARCH_TABLE, TICKER_TABLE, DROP_TABLE

class KeywordsearchPipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect('./' + DB + '.db')
        self.cur = self.conn.cursor()
        if DROP_TABLE:
            self.cur.execute('DROP TABLE IF EXISTS ' + SEARCH_TABLE)
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + SEARCH_TABLE +
                         '''(
                         title TEXT,
                         author TEXT,
                         keyline TEXT,
                         time TEXT,
                         publisher TEXT,
                         url TEXT,
                         query TEXT,
                         content TEXT);''')
    
    def __del__(self):
        self.conn.close()
        
    def process_item(self, item, spider):
        if spider.name == 'yfnc':
            return item
        if len(item) != 8:
            raise Exception('Item has incorrect number of attributes!')
        
        for k, v in item.iteritems():
            if isinstance(v, list):
                item[k] = ''.join(v)
        self.cur.execute('INSERT INTO ' + SEARCH_TABLE + ' VALUES(?,?,?,?,?,?,?,?)',
                         (item['title'], item['author'], item['keyLine'], item['time'], item['publisher'], item['url'], item['query'], item['content']))
        self.conn.commit()
        return item


class YahoofinancePipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect('./' + DB + '.db')
        self.cur = self.conn.cursor()
        if DROP_TABLE:
            self.cur.execute('DROP TABLE IF EXISTS ' + TICKER_TABLE)
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + TICKER_TABLE +
                         '''(
                         date INTEGER PRIMARY KEY,
                         open NUMERIC,
                         high NUMERIC,
                         low NUMERIC,
                         close NUMERIC,
                         volume INTEGER,
                         adjClose NUMERIC);''')
    
    def __del__(self):
        self.conn.close()
        
    def process_item(self, item, spider):
        if spider.name != 'yfnc':
            return item
        if len(item) != 7: # avoid dividend line
            return
        self.cur.execute('INSERT INTO ' + TICKER_TABLE + ' VALUES(?,?,?,?,?,?,?)',
                         (item['date'], item['open'], item['high'], item['low'], item['close'], item['volume'], item['adjClose']))
        self.conn.commit()
        return item