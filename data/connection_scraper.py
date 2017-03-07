from db import DB
import urllib
import re
from textblob import TextBlob
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from text_parser import TextParser

db = DB()
parser = TextParser()

def is_politician(name):
    row = db.get_entity(name)
    return len(row) > 0

def get_sentances(p):
    if p.getText() is None:
        return []
    blob = TextBlob(p.getText())
    return blob.raw_sentences

def scrape_page(url):
    response = urllib.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find('div', {'id': 'bodyContent'})
    for script in soup(["script", "style"]):
        script.extract()

    for p in soup.find_all('p'):
        sentances = get_sentances(p)
        soup_sentances = []
        for s in sentances:
            if len(s) <= 1:
                continue
            
            def get_sentence(v):
                print v
                return True
            soup_sentances.append(p.find_all(string=get_sentence))
         
        sents = [val for sublist in soup_sentances for val in sublist]
        for s in sents:
            if isinstance(s, NavigableString):
                continue
            for a in s.find_all('a'):
                href = a['href']
                name = re.match(r'/wiki/(\w+)', href)
                print name
                if name:
                    if is_politician(name):
                        print s
                        cat = parser.classify(s.getText())
                        # insert connection into database here

def scrape():
    rows = db.get_rows()
    for row in rows:
        scrape_page(row[2])

if __name__ == '__main__':
    scrape()
