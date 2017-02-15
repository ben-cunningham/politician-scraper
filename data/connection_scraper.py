from db import DB
from bs4 import BeautifulSoup
import urllib

db = DB()

def scrape_page(url):
    response = urllib.urlopen(url)

def scrape():
    rows = db.get_rows()
    for row in rows:
        scrape_page(row[2])

if __name__ == '__main__':
    scrape()
