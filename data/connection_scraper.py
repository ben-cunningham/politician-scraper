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
    return blob.sentences

def get_wiki_url(phrase):
    pass

def is_wiki_page(data):
    pass

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
            #soup_sentances.append(p.find_all(string=get_sentence))
            #foo = p.find(string=re.compile('President of the United States</a> in the'))
            nouns = s.noun_phrases
            #print nouns
            for noun in nouns:
                pass

def scrape():
    rows = db.get_rows()
    for row in rows:
        scrape_page(row[2])

if __name__ == '__main__':
    scrape()
