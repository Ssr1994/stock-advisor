# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from stockadvisor.items import YahoofinanceItem, YfncItemFields

class YfncSpider(scrapy.Spider):
    name = "yfnc"
    allowed_domains = ["yahoo.com"]
    basic_url = "http://finance.yahoo.com/q/hp?s="
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ticker = "MSFT"

    def start_requests(self):
        yield scrapy.Request(self.basic_url + self.ticker + '+Historical+Prices', self.parse)
    
    def parse(self, response):
        for tr in response.xpath('//table[@class="yfnc_datamodoutline1"]//table/tr')[1:-1]:
            item = YahoofinanceItem()
            for i, td in enumerate(tr.xpath('td/text()').extract()):
                item[YfncItemFields[i]] = td
            if len(item) == 7:
                sd = item['date'].split()
                item['date'] = date(int(sd[2]), self.months.index(sd[0]) + 1, int(sd[1][0:-1])).strftime('%Y%m%d')
                item['volume'] = item['volume'].replace(',', '')
            yield item