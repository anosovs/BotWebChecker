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

def put_expiration_date(domain, exp_date):
    values = (exp_date, domain)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    query = '''
            UPDATE exp_check
            SET exp_date = (?)
            WHERE site_id = (SELECT site_id
                            FROM sites
                            WHERE domain = (?)
                            )
            '''
    cur.execute(query, values)
    con.commit()
    con.close()

def put_test_values():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    tested_domains = []
    try:
        with open('../test-domains.txt', 'r') as f:
            for el in f:
                tested_domains.append([el.strip()])
        sql_req = [
            '''INSERT INTO sites (domain) VALUES(?)''',
            '''INSERT INTO status_check (status_check, site_id)
                VALUES(true, (SELECT site_id FROM sites WHERE domain=(?)))''',
            '''
                INSERT INTO exp_check (exp_check, site_id)
                VALUES(true, (SELECT site_id FROM sites WHERE domain=?))''',
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

def add_domain(domain):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    domain = [domain]
    sql_req = [
        '''INSERT INTO sites (domain) VALUES(?)''',
        '''INSERT INTO status_check (status_check, site_id)
            VALUES(true, (SELECT site_id FROM sites WHERE domain=(?)))''',
        '''
            INSERT INTO exp_check (exp_check, site_id)
            VALUES(true, (SELECT site_id FROM sites WHERE domain=?))''',
    ]
    for sql in sql_req:
        cur.execute(sql, domain)
    con.commit()
    con.close()

def del_domain(domain):
    sql_req = '''
        DELETE FROM sites
        WHERE site_id=(?) OR domain=(?)
    '''
    values = (domain, domain)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    con.commit()
    con.close()

def get_all_domains():
    sql_req = '''
        SELECT site_id, domain
        FROM sites
    '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req)
    domains = cur.fetchall()
    con.commit()
    con.close()
    return domains

def toggle_status_check(domain):
    sql_req = '''
            UPDATE status_check
            SET status_check = CASE status_check
                                WHEN 1 THEN 0
                                ELSE 1
                                END
            WHERE site_id = (
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    con.commit()
    con.close()

def is_on_status_check(domain):
    sql_req = '''
            SELECT status_check
            FROM status_check
            WHERE site_id=(
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    result = cur.fetchone()
    con.commit()
    con.close()
    if result[0] == 1:
        return 1
    else:
        return 0


def toggle_exp_check(domain):
    sql_req = '''
            UPDATE exp_check
            SET exp_check = CASE exp_check
                                WHEN 1 THEN 0
                                ELSE 1
                                END
            WHERE site_id = (
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    con.commit()
    con.close()

def is_on_exp_check(domain):
    sql_req = '''
            SELECT exp_check
            FROM exp_check
            WHERE site_id=(
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    result = cur.fetchone()
    con.commit()
    con.close()
    if result[0] == 1:
        return 1
    else:
        return 0

def toggle_tag_check(domain):
    is_available = is_on_tag_check(domain)
    print(is_available)
    if is_available == 1:
        sql_req = '''
            UPDATE tag_check
            SET tag_check = CASE tag_check
                                WHEN 1 THEN 0
                                ELSE 1
                                END
            WHERE site_id = (
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    elif is_available == 0:
        sql_req = '''
                    UPDATE tag_check
                    SET tag_check = CASE tag_check
                                        WHEN 1 THEN 0
                                        ELSE 1
                                        END
                    WHERE site_id = (
                                    SELECT site_id
                                    FROM sites
                                    WHERE site_id=(?) OR domain=(?)
                    )
                '''
    else:
        print('third')
        sql_req = '''
                INSERT INTO tag_check (tag_check, site_id)
                VALUES (1, (SELECT site_id
                                FROM sites
                                WHERE site_id=(?) OR domain=(?)))
            '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    con.commit()
    con.close()

def is_on_tag_check(domain):
    sql_req = '''
            SELECT tag_check
            FROM tag_check
            WHERE site_id=(
                            SELECT site_id
                            FROM sites
                            WHERE site_id=(?) OR domain=(?)
            )
        '''
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    values = (domain, domain)
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(sql_req, values)
    result = cur.fetchone()
    con.commit()
    con.close()
    if result is None:
        return None
    if result[0] == 1:
        return 1
    elif result[0] == 0:
        return 0
    else:
        return None

