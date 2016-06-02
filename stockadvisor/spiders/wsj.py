# -*- coding: utf-8 -*-
import scrapy
import urllib
from stockadvisor.items import KeywordsearchItem
from stockadvisor.settings import QUERY
from stockadvisor.outputwebpage import outputWebpage

class WsjSpider(scrapy.Spider):
    name = "wsj"
    allowed_domains = ["wsj.com"]
    basic_url = "http://www.wsj.com/search/term.html?KEYWORDS="
    query = None

    def start_requests(self):
        yield scrapy.Request(self.basic_url + urllib.quote(self.query), self.parse)
    
    def parse(self, response):
        for url in response.xpath('//h3[@class="headline"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_article, headers={'Referer': 'https://www.google.com'})
    
    def parse_article(self, response):
        item = KeywordsearchItem()
        if response.url.split('/')[3] == 'cio': #http://.../cio/...
            header = response.xpath('//header[@class="post-header single-post-header"]')
            item['title'] = header.xpath('h1[@class="post-title h-main"]/text()').extract()
            item['time'] = ' '.join(header.xpath('small[@class="post-time"]/text()').extract())
            item['keyLine'] = ''
            body = response.xpath('//div[@class="post-content"]')
            item['author'] = body.xpath('//li[@class="post-author"]/a/text()').extract()
            item['content'] = ' '.join(body.xpath('p//text()').extract())
        else:
            item['title'] = response.xpath('//h1[@class="wsj-article-headline"]/text()').extract()
            item['keyLine'] = response.xpath('//h2[@class="sub-head"]/text()').extract()
            body = response.xpath('//div[@id="wsj-article-wrap"]')
            item['author'] = body.xpath('//span[@itemprop="name"]/text()').extract()
            item['time'] = body.xpath('//time[@class="timestamp"]/text()').extract()
            item['content'] = ' '.join(body.xpath('p//text()').extract())
        item['title'] = ''.join(item['title']).lstrip()
        item['url'] = response.url
        item['publisher'] = 'WSJ'
        item['query'] = self.query
        #outputWebpage(item['title'], response)
        yield item