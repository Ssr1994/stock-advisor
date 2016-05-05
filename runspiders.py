from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stockadvisor.settings import FILE_PATH
import os

def run_spiders(query=None, ticker=None):
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    
    #settings = get_project_settings()
    #settings.setdict({'QUERY': query, 'TICKER': ticker, 'DB': db, 'SEARCH_TABLE': searchTable, 'TICKER_TABLE': tickerTable})
    process = CrawlerProcess(get_project_settings())
    if query:
        process.crawl('cnn', query=query)
        process.crawl('foxnews', query=query)
        process.crawl('latimes', query=query)
        process.crawl('nytimes', query=query)
        process.crawl('wapost', query=query)
        process.crawl('wsj', query=query)
    if ticker:
        process.crawl('yfnc', ticker=ticker)
    process.start()
        