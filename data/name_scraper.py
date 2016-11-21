from bs4 import BeautifulSoup
import urllib

WIKI_URL_21 = 'https://en.wikipedia.org/w/index.php?title=Category:21stj-century_American_politicians'
WIKI_URL_20 = 'https://en.wikipedia.org/w/index.php?title=Category:20th-century_American_politicians'

urls= []
names = {}

def check_politician(entity):
    pass

def scrape(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    

if __name__ == '__main__':
    scrape(WIKI_URL_21)
    scrape(WIKI_URL_20)
