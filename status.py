from webchecker import Webchecker
from settings import *
import common_func
import sqlite3
import datetime

def take_status_query(db=DATABASE):
    """
    Taking all domains for status check
    :param db: database
    :return: list of available domains
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''
    SELECT status_check, domain
    FROM status_check
    INNER JOIN sites USING (site_id)
    WHERE status_check = 1
    ''')
    all_query = cur.fetchall()
    result = []
    for query in all_query:
        if query[0]==1:
            result.append(query[1])
    con.commit()
    con.close()
    return result


if __name__ == "__main__":
    failed_status_of_domain = []
    message = f'{common_func.get_beaty_now()}\n'
    wc = Webchecker()
    # Main try for checking
    for el in take_status_query():
        status = wc.check_status(el)
        if status != 200:
            if status != 200:
                if status == 999:
                    message += f'Can\'t check http://{el}.\n'
                else:
                    message += f'Failed: http://{el}/. Status {wc.check_status(el)}\n'
    message += f'{common_func.get_beaty_now()}'
