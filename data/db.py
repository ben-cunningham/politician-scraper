import os.path
import psycopg2
import configparser

connection = None

def create_tables():
    pass
    
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config.get('Database config', 'DATABASE_URL')
    print url
    # create_table()
    # data = get_info()
    
