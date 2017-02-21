from db import DB
import urllib
import re
from bs4 import BeautifulSoup
from text_parser import TextParser

db = DB()
parser = TextParser()

def is_politician(url):
    return True

def get_sentances(p):
    return p.string.split('.')

def scrape_page(url):
    response = urllib.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find('div', {'id': 'bodyContent'})
    for script in soup(["script", "style"]):
        script.extract()

    for p in soup.find_all('p'):
        sentances = get_sentances(p)
        for s in sentances:
            for a in s.find_all('a'):
                href = a['href']
                name = re.match(r'/wiki/(\w+)', href)
                if name:
                    if is_politician(name):
                        cat = parser.classify(s.getText())
                        # insert connection into database here

def scrape():
    rows = db.get_rows()
    for row in rows:
        scrape_page(row[2])

if __name__ == '__main__':
    scrape()
