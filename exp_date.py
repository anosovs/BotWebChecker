import whois
import sqlite3
import datetime
import common_func
import databaseworker
from webchecker import Webchecker
from settings import *


def take_expdate_query(db=DATABASE):
    """
    Taking all domains for expired date check
    :param db: database
    :return: list of domains for checking expired date
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''
    SELECT exp_check, exp_date, domain
    FROM exp_check
    INNER JOIN sites USING (site_id)
    WHERE exp_check = 1
    ''')
    all_query = cur.fetchall()
    result = []
    for query in all_query:
        if query[0] == 1:
            result.append((query[1], query[2]))
    con.commit()
    con.close()
    return result


if __name__ == "__main__":
    message = f'Start: {common_func.get_beaty_now()}\n'
    wc = Webchecker()
    # If db have exp date we check it from db, if date so close to warn we check it in whois service
    # and in this case date will compare
    # If db don't have exp date we gonna take info from whois service, compare and put into db
    for el in take_expdate_query():
        if el[0] is not None:
            diff_date = datetime.datetime.strptime(el[0], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
            if diff_date.days <= WARN_ADVANCE:
                exp_date = wc.get_expiration_date(el[1])
                if (exp_date != -1) and (exp_date is not None):
                    diff_date_second = exp_date - datetime.datetime.now()
                    if diff_date_second.days <= WARN_ADVANCE:
                        message += f'Domain {el[1]} expired in {diff_date_second.days} day(s)\n'
                else:
                    message += f'Can\'t check expiration date for {el[1]}\n'
        else:
            exp_date = wc.get_expiration_date(el[1])
            if (exp_date != -1) and (exp_date is not None):
                # writting to db
                databaseworker.put_expiration_date(el[1], exp_date)
                diff_date_second = exp_date - datetime.datetime.now()
                if diff_date_second.days <= WARN_ADVANCE:
                    message += f'Domain {el[1]} expired in {diff_date_second.days} day(s)\n'
            else:
                message += f'Can\'t check expiration date for {el[1]}\n'
    # Sending
    message += f'End: {common_func.get_beaty_now()}'
    for chat_id in CHAT_IDS:
        common_func.send_telegram(chat_id, message)
