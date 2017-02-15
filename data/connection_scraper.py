from db import DB

db = DB()

def scrape_page(page):
    rows = db.get_rows()

if __name__ == '__main__':
    scrape_page(None)
