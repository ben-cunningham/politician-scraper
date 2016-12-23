import os.path
import psycopg2
import configparser
import urlparse

from queries import Queries

conn = None

def create_tables():
    cur = conn.cursor()
    cur.execute(Queries.create_edge)
    cur.execute(Queries.create_vertex)
    cur.close()
    
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config.get('Database config', 'DATABASE_URL')
    
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(url)
    
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    
    create_tables()
    conn.commit()
    conn.close() 
