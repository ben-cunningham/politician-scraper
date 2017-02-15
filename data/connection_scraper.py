from db import DB

db = DB()

def scrape(page):
    rows = db.get_rows()

if __name__ == '__main__':
    scrape(None)
