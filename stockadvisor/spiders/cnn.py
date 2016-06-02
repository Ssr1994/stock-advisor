# -*- coding: utf-8 -*-
import scrapy
import urllib
from stockadvisor.items import KeywordsearchItem
from stockadvisor.settings import QUERY
from stockadvisor.outputwebpage import outputWebpage

class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["cnn.com"]
    basic_url = "http://www.cnn.com/search/?text="
    query = None

    def start_requests(self):
        if not self.query:
            self.query = QUERY
        # CNN's date range is handled in middlewares.py
        for n in [1, 2]:
            yield scrapy.Request(self.basic_url + urllib.quote_plus(self.query), self.parse, dont_filter=True,
                                 meta={"phantomjs": True, 'target': 'cnn', 'pageNum': n})
    
    def parse(self, response):
        for url in response.xpath('//h3[@class="cd__headline"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)
    
    def parse_article(self, response):
        urlSplit = response.url.split('/')
        if urlSplit[3] == 'videos':
            return
        
        item = KeywordsearchItem()
        if urlSplit[6] == 'opinions':
            item['title'] = response.xpath('//h1[@class="pg-headline"]/text()').extract()
            item['author'] = response.xpath('//span[@class="metadata__byline__author"]/a/text()').extract()
            item['time'] = response.xpath('//p[@class="update-time"]/text()').extract()
            item['keyLine'] = ''
            item['content'] = ' '.join(response.xpath('//p[@class="zn-body__paragraph"]//text()').extract())
        else:
            item['title'] = response.xpath('//h1[@class="article-title"]/text()').extract()
            item['author'] = response.xpath('//span[@class="cnnbyline "]/span[@class="byline"]/a/text()').extract()
            body = response.css('#storytext')
            item['keyLine'] = body.xpath('h2/text()').extract()
            item['content'] = ' '.join(body.xpath('p//text()').extract())
            item['time'] = response.xpath('//div[@class="storytimestamp"]/span[@class="cnnDateStamp"]/text()').extract()
        item['url'] = response.url
        item['publisher'] = 'CNN'
        item['query'] = self.query
        item['title'] = ''.join(item['title'])
        #outputWebpage(item['title'], response)
        yield item