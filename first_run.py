import requests
import json
from libs.databaseworker import create_db
import os

with open('settings.py', 'w') as f:
    if os.path.isfile('dbwebcheker.db'):
        dbanswer = input('You already have dbwebcheker, do you want create NEW EMPTY db? (y or n)\n').strip()
        if dbanswer == 'y':
            f.write("DATABASE = 'dbwebcheker.db'\n")
            try:
                create_db()
                print('Empty sqlite dabatabe generated')
            except:
                print('Can\'t generated Sqlite database')
        else:
            print('New database not created')
    else:
        f.write("DATABASE = 'dbwebcheker.db'\n")
        try:
            create_db()
            print('Empty sqlite dabatabe generated')
        except:
            print('Can\'t generated Sqlite database')
    api = input('Ask @BotFather and enter API token for telegram: ')
    f.write(f"API_TOKEN = '{api}'\n")
    print('Write "/chat_id" to your telegram bot')
    chat_id = ''
    while chat_id=='':
        try:
            req = requests.get(f'https://api.telegram.org/bot{api}/getUpdates')
            tmp = json.loads(req.text)
            chat_id = tmp['result'][0]['message']['chat']['id']
            print('chat_id Added successfully')
        except:
            continue
    f.write(f"CHAT_IDS = ['{chat_id}']\n")
    warn_before = input('How long do need to warn you about domain expiration: ')
    f.write(f'WARN_ADVANCE = {warn_before}\n')
    print('Settings complete')