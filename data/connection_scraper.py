from db import DB
import re, json, urllib
from textblob import TextBlob
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from text_parser import TextParser

db = DB()
parser = TextParser()

WIKIPEDIA_SEARCH_URL = \
    "https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search="

def get_entity(name):
    row = db.get_entity(name)
    if len(row) > 0 and len(row[0]) > 0:
        return row[0][0]
    return ''

def is_politician(name):
    row = db.get_entity(name)
    return len(row) > 0

def insert_connection(e1, e2, inf, cls=-1):
    db.insert_edge(e1, e2, inf, cls)

def get_sentances(p):
    if p.getText() is None:
        return []
    blob = TextBlob(p.getText())
    return blob.sentences

def get_wiki_url(phrase):
    res = urllib.urlopen(WIKIPEDIA_SEARCH_URL +str(phrase.encode('ascii', 'ignore'))).read()
    res =  json.loads(res)
    if len(res) >= 4:
        if len(res[3]) > 0:
            return res[3][0]

    return ""

def get_name_from_url(url):
    name = re.search(r'/wiki/(\w+)', url)
    if name:
        return name.group(1)
    return None

def clean_sentance(sent):
    s = re.sub(r'\[[0-9]+\]', '', sent)
    return s

def scrape_page(e1, url):
    response = urllib.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find('div', {'id': 'bodyContent'})
    for script in soup(["script", "style"]):
        script.extract()

    e1 = get_entity(e1)
    # scrape the body of the wiki page
    for p in soup.find_all('p'):
        sentances = get_sentances(p)
        soup_sentances = []
        for s in sentances:
            if len(s) <= 1:
                continue
            nouns = s.noun_phrases
            for noun in nouns:
                url = get_wiki_url(noun)
                name = get_name_from_url(url)
                if name and is_politician(name):
                    e2 = get_entity(name)
                    if e1 == e2:
                        continue
                    inf = {
                        'sentence': clean_sentance(str(s))
                    }

                    print e1, e2, inf
                    # insert_connection(e1, e2, inf,  cls)

def scrape():
    rows = db.get_rows()
    for row in rows:
        scrape_page(row[1], row[2])

if __name__ == '__main__':
    scrape()
