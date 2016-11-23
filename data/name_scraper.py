from bs4 import BeautifulSoup

import urllib
import re

BASE_URL = 'https://en.wikipedia.org'
WIKI_URL_21 = 'https://en.wikipedia.org/w/index.php?title=Category:21st-century_American_politicians'
WIKI_URL_20 = 'https://en.wikipedia.org/w/index.php?title=Category:20th-century_American_politicians'

urls= []
names = {}

def check_politician(entity):
    pass

def scrape(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1', {'id': 'firstHeading'}).getText()
    
    content = soup.find('div', {'id': 'bodyContent'})
    for a in content.find_all('a'):
        href = a['href']
        name = re.match(r'/wiki/(\w+)', href)
        if name:
            article = name.group(1)

if __name__ == '__main__':
    html = urllib.urlopen(WIKI_URL_21).read()
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', { 'id': 'mw-pages' })
    for group in pages.find_all('div', {'class': 'mw-category-group'}):
        for link in group.find_all('a'):
            scrape(BASE_URL + link['href'])
