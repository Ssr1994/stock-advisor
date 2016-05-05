import re
from stockadvisor.settings import FILE_PATH

def outputWebpage(title, response):
    with open(FILE_PATH + re.sub('[:/]', '', title) + '.html', 'w') as f:
        f.write(response.body)