# -*- coding: utf-8 -*-
import scrapy
import urllib
from datetime import date, timedelta
from stockadvisor.items import KeywordsearchItem
from stockadvisor.settings import QUERY
from stockadvisor.outputwebpage import outputWebpage

class LatimesSpider(scrapy.Spider):
    name = "latimes"
    allowed_domains = ['latimes.com']
    query_url = "http://www.latimes.com/search/dispatcher.front?Query="
    query = None
    days = 30

    def start_requests(self):
        if not self.query:
            self.query = QUERY
        end_date = date.today()
        start_date = end_date - timedelta(self.days)
        options = "&target=all&spell=on&date=" + start_date.strftime('%m/%d/%Y') + "-" + end_date.strftime('%m/%d/%Y')
        for n in ['1', '2']:
            yield scrapy.Request(self.query_url + urllib.quote_plus(self.query) + options + '&page=' + n, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//div[@class="trb_search_result_wrapper"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article)

    def parse_article(self, response):
        item = KeywordsearchItem()
        item['title'] = response.xpath('//div[@class="trb_ar_hl"]/h1/text()').extract()
        if not item['title']:
            item['title'] = response.xpath('//div[@class="trb_article_title"]/h1/text()').extract()

        item['author'] = response.xpath('//span[@class="trb_ar_by_nm_au"]/a/text()').extract()
        if not item['author']:
            item['author'] = response.xpath('//span[@class="trb_bylines_nm_au"]/a/text()').extract()    
        if not item['author']:
            item['author'] = response.xpath('//span[@class="trb_ar_by_nm_au"]/span/text()').extract()

        item['time'] = response.xpath('//div[@class="trb_ar_dateline"]/time/@data-dt').extract()
        if not item['time']:
            item['time'] = response.xpath('//div[@class="trb_article_dateline"]/time/@data-dt').extract()
        
        item['publisher'] = "LATimes"
        item['url'] = response.url

        item['content'] = ' '.join(response.xpath('//div[@class="trb_ar_page"]/p//text()').extract())
        if not item['content']:
            item['content'] = ' '.join(response.xpath('//div[@id="story"]/p//text()').extract())
        if not item['content']:
            item['content'] = ' '.join(response.xpath('//div[@id="liveblog-description"]/p//text()').extract())
        item['query'] = self.query
        item['keyLine'] = ''
        item['title'] = ''.join(item['title']).lstrip().rstrip()
        #outputWebpage(item['title'], response)
        yield item
