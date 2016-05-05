# -*- coding: utf-8 -*-
import scrapy
import urllib
from stockadvisor.items import KeywordsearchItem
from stockadvisor.settings import QUERY
from stockadvisor.outputwebpage import outputWebpage

class WapostSpider(scrapy.Spider):
    name = "wapost"
    allowed_domains = ["washingtonpost.com"]
    basic_url = 'http://www.washingtonpost.com/newssearch/?query='
    date_range = '7+Days'

    def start_requests(self):
        yield scrapy.Request(self.basic_url + urllib.quote_plus(QUERY) + '&datefilter=' + self.date_range, self.parse,
                             meta={"phantomjs": True, "target": 'wapost'})
    
    def parse(self, response):
        for url in response.xpath('//div[@class="pb-results-container"]//a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)
    
    def parse_article(self, response):
        #may have duplicate articles under different topics
        #check back http://www.washingtonpost.com/sf/brand-connect/microsoft/wp/enterprise/government-cybersecurity-imperative-a-microsoft-perspective/
        item = KeywordsearchItem()
        item['title'] = ''.join(response.xpath('//div[@id="article-topper"]//h1/text()').extract()).lstrip()
        body = response.xpath('//div[@id="article-body"]')
        item['author'] = body.xpath('//span[@itemprop="name"]/text()').extract()
        item['time'] = body.xpath('//span[@itemprop="datePublished"]/text()').extract()
        item['publisher'] = 'WP'
        item['url'] = response.url
        item['content'] = ' '.join(body.xpath('article[@itemprop="articleBody"]/p//text()').extract())
        item['query'] = QUERY
        item['keyLine'] = ''
        outputWebpage(item['title'], response)
        yield item