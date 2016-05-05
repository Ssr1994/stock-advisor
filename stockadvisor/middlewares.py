from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
import time

class PhantomJSMiddleware(object):
    
    def process_request(self, request, spider):
        if request.meta.get('phantomjs', False):
            driver = webdriver.PhantomJS(executable_path='phantomjs', service_args=['--load-images=no'])
            driver.get(request.url)
            if request.meta.has_key('target'):
                if request.meta['target'] == 'wapost':
                    btn = driver.find_element_by_css_selector('div.pb-loadMore')
                    if btn.is_displayed():
                        btn.click()
                elif request.meta['target'] == 'cnn':
                    if int(request.meta['pageNum']) == 1:
                        driver.execute_script('document.getElementById("PASTMONTH").click();')
                    else:
                        driver.execute_script('document.getElementById("PASTMONTH").click(); el = document.getElementsByClassName("left text text-active"); if (el.length) el[0].click();')
            time.sleep(3)
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.close()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)
        else:
            return None


class MyRedirectMiddleware(RedirectMiddleware):

    def process_response(self, request, response, spider):
        if spider.name == 'nytimes':
            return response
        else:
            return super(MyRedirectMiddleware, self).process_response(request, response, spider)