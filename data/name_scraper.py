from bs4 import BeautifulSoup
import urllib

WIKI_URL_21 = 'https://en.wikipedia.org/w/index.php?title=Category:21st-century_American_politicians'
WIKI_URL_20 = 'https://en.wikipedia.org/w/index.php?title=Category:20th-century_American_politicians'

urls= []
names = {}

def check_politician(entity):
    pass

def scrape(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

if __name__ == '__main__':
    html = urllib.urlopen(WIKI_URL_21).read()
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', { 'id': 'mw-pages' })
    for group in pages.find_all('div', {'class': 'mw-category-group'}):
        for link in group.find_all('a'):
            print link['href']
