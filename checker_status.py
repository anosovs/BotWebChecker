from libs.webchecker import Webchecker
from settings import *
from libs import common_func
import sqlite3

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
    statusForSend = False
    message = f'Start: {common_func.get_beaty_now()}\n'
    wc = Webchecker()
    for el in take_status_query():
        status = wc.check_status(el)
        if status != 200:
            statusForSend = True
            if status == 999:
                message += f'Can\'t check http://{el}.\n'
            else:
                message += f'Failed: http://{el}/. Status {wc.check_status(el)}\n'
    message += f'End: {common_func.get_beaty_now()}'
    with open('logs/status_last.txt', 'w') as f:
        f.write(message)
    if statusForSend:
        for chat_id in CHAT_IDS:
            common_func.send_telegram(chat_id, message)