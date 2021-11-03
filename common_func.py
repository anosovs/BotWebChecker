import settings
import requests
import datetime


def send_telegram(chat_id, message):
    message = [message[i:i+3000] for i in range(0, len(message), 3000)]
    for msg in message:
        send_text = 'https://api.telegram.org/bot' + settings.API_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + msg
        response = requests.get(send_text)
    return response.json()

def get_beaty_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")