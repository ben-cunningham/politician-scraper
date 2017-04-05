import re, json, urllib
import asyncio, aiohttp, async_timeout

from db import DB
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
    a = db.get_edge(e1, e2)
    b = db.get_edge(e2, e1)

    if len(a) > 0:
        db.update_edge(e1, e2, a[0][2] +"|" +inf["sentence"])
    elif len(b) > 0:
        db.update_edge(e2, e1, b[0][2] +"|" +inf["sentence"])
    else:
        db.insert_edge(e1, e2, inf['sentence'], cls)

def get_sentances(p):
    if p.getText() is None:
        return []
    blob = TextBlob(p.getText())
    return blob.sentences

async def get_wiki_url(session, phrase):
    with async_timeout.timeout(1000):
        url = WIKIPEDIA_SEARCH_URL +phrase 
        async with session.get(url) as response:
            res = await response.json()
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

async def scrape_page(session, e1, url):
    async with session.get(url) as response:
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')
        soup = soup.find('div', {'id': 'bodyContent'})
        for script in soup(["script", "style"]):
            script.extract()

        e1 = get_entity(e1).strip()
        # scrape the body of the wiki page
        for p in soup.find_all('p'):
            sentances = get_sentances(p)
            soup_sentances = []
            for s in sentances:
                if len(s) <= 1:
                    continue
                nouns = s.noun_phrases
                for noun in nouns:
                    try:
                        url = await get_wiki_url(session, noun)
                    except asyncio.TimeoutError:
                        print('could not get wiki url for ' +str(noun))
                        continue
                    name = get_name_from_url(url)
                    if name and is_politician(name):
                        e2 = get_entity(name).strip()
                        if e1 == e2:
                            continue
                        inf = {
                            'sentence': clean_sentance(str(s))
                        }
                        
                        try:
                            insert_connection(e1, e2, inf)
                        except:
                            print('couldn\'t insert connection for name')


async def scrape(loop):
    print("Connecting to database")
    rows = db.get_rows()
    async with aiohttp.ClientSession(loop=loop) as session:
         await asyncio.gather(
             *[scrape_page(session, row[1], row[2]) for row in rows]
         )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape(loop))
