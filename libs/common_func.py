import settings
import requests
import datetime
import re


def send_telegram(chat_id, message):
    message = [message[i:i+3000] for i in range(0, len(message), 3000)]
    for msg in message:
        send_text = 'https://api.telegram.org/bot' + settings.API_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + msg
        response = requests.get(send_text)
    return response.json()

def get_beaty_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_correct_domain(name):
    '''

    :param name: name of domain
    :return: if its domain return re.object in other case None
    '''
    regex = r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]'
    return re.match(regex, name)

def type_of_input(namestr):
    '''

    :param namestr:
    :return: str domain or id or wrong
    '''
    if is_correct_domain(namestr):
        return 'domain'
    elif str.isdigit(namestr):
        return 'id'
    else:
        return 'wrong'