from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stockadvisor.settings import FILE_PATH
import os

def run_spiders(query=None, ticker=None):
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    
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

import sys, getopt

if __name__ == "__main__":
    query = None
    ticker = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hq:t:")
    except getopt.GetoptError:
        print 'runspiders.py -q <query> -t <ticker>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'runspiders.py -q <query> -t <ticker>'
            sys.exit()
        elif opt == '-q':
            query = arg
        elif opt == '-t':
            ticker = arg
    run_spiders(query, ticker)