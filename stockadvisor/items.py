# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class KeywordsearchItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    keyLine = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    publisher = scrapy.Field()
    url = scrapy.Field()
    query = scrapy.Field()

class YahoofinanceItem(scrapy.Item):
    date = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    adjClose = scrapy.Field()
    company = scrapy.Field()

YfncItemFields = ['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose'] # must be consistent with the order in the item class