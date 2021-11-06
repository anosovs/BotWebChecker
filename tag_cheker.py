from webchecker import Webchecker
import sqlite3
from settings import *
import common_func


def take_tag_query(db=DATABASE):
    """
    Taking all domains for existing tag check
    :param db: database
    :return: list of domains for checking existing tag
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''
    SELECT tag_check, tag_text, domain
    FROM tag_check
    INNER JOIN sites USING (site_id)
    WHERE tag_check = 1
    ''')
    all_query = cur.fetchall()
    result = []
    for query in all_query:
        if query[0] == 1:
            result.append((query[2], query[1]) )
    con.commit()
    con.close()
    return result


if __name__ == '__main__':
    statusForSend = False
    message = f'Start: {common_func.get_beaty_now()}\n'
    wc = Webchecker()
    for query in take_tag_query():
        if wc.check_tag(query[0], query[1]) == -1:
            statusForSend = True
            message += f'Tag {query[1]} not found on {query[0]}\n'
    message += f'End: {common_func.get_beaty_now()}'
    with open('tag_last.txt', 'w') as f:
        f.write(message)
    if statusForSend:
        for chat_id in CHAT_IDS:
            common_func.send_telegram(chat_id, message)