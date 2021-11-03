import sqlite3
from settings import *


# CREATE TEST STRUCTURE OF DB
def create_db():
    open(DATABASE, 'w').close()
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute('''
    CREATE TABLE sites
        (site_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        domain VARCHAR(255) NOT NULL)
    ''')
    cur.execute('''
    CREATE TABLE status_check
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        status_check BOOLEAN,
        site_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (site_id) references sites(site_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
        )
    ''')
    cur.execute('''
    CREATE TABLE exp_check
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        exp_check BOOLEAN,
        exp_date DATE,
        site_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (site_id) references sites(site_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
        )
    ''')
    cur.execute('''
    CREATE TABLE tag_check
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tag_check BOOLEAN,
        tag_text TEXT,
        site_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (site_id) references sites(site_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
        )
    ''')
    cur.execute('''
    CREATE TABLE delay
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        delay_untill DATE,
        site_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (site_id) references sites(site_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
        )
    ''')
    cur.execute('''
    CREATE TABLE contacts
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(255),
        phone VARCHAR(15),
        email VARCHAR(80),
        site_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (site_id) references sites(site_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
        )
    ''')

    con.commit()
    con.close()


def put_test_values():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    tested_domains = []
    try:
        with open('test-domains.txt', 'r') as f:
            for el in f:
                tested_domains.append([el.strip()])
        sql_req = [
            '''INSERT INTO sites (domain) VALUES(?)''',
            '''INSERT INTO status_check (status_check, site_id)
                VALUES(true, (SELECT site_id FROM sites WHERE domain=(?)))
                ''',
            '''
                INSERT INTO exp_check (exp_check, site_id)
                VALUES(true, (SELECT site_id FROM sites WHERE domain=?))
                ''',
        ]
        for sql in sql_req:
            for el in tested_domains:
                cur.execute(sql, (el))
    except:
        print('file with tested domains not found')
    # random
    domain = ['ajsfhdf.com']
    cur.execute('''
        INSERT INTO sites (domain)
        VALUES(?)
        ''', domain)
    cur.execute('''
        INSERT INTO status_check (status_check, site_id)
        VALUES(true, (SELECT site_id FROM sites WHERE domain=?))
        ''', domain)
    cur.execute('''
        INSERT INTO exp_check (exp_check, site_id)
        VALUES(true, (SELECT site_id FROM sites WHERE domain=?))
        ''', domain)
    con.commit()
    con.close()


if __name__ == "__main__":
    create_db()
    put_test_values()
