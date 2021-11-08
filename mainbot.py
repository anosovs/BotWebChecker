from settings import *
from libs import common_func as cf, databaseworker as dbw
import telebot

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(commands=['start', 'help', 'commands'])
def start(message):
    if str(message.chat.id in CHAT_IDS):
        bot.send_message(message.chat.id, f'/add <domain>- add domain\n'
                                          f'/del <domain or ID> - delete domain (use id or domain name)\n'
                                          f'/domains - list of available domains with id'
                                          f'/status_check <domain or ID> - toggle check for status\n'
                                          f'/exp_check <domain or ID> - toggle expiration date check\n'
                                          f'/tag_check <domain or ID> - check existing of tag on index page\n'
                                          f'/tag <domain or ID> - add\\change tag for domain\n'
                                          f'/last - return result of last check\n'
                                          f'/chat_id - available for everybody return chat_id')


@bot.message_handler(commands=['add'])
def add_domain(message):
    msg = message.text.replace('/add ', '').strip()
    if cf.is_correct_domain(msg) is not None:
        try:
            dbw.add_domain(msg)
            bot.send_message(message.chat.id, f'Domain {msg} added. Checking status ON, expiration date ON, tag OFF')
        except:
            bot.send_message(message.chat.id, 'Something gonna wrong when adding domain')
    else:
        bot.send_message(message.chat.id, f'Uncorrected domain - {msg}')


@bot.message_handler(commands=['del'])
def del_domain(message):
    msg = message.text.replace('/del ', '').strip()
    if cf.type_of_input(msg) == 'domain' or cf.type_of_input(msg) == 'id':
        try:
            dbw.del_domain(msg)
            bot.send_message(message.chat.id, f'Successfully deleted {msg}')
        except:
            bot.send_message(message.chat.id, f'Can\'t delete {msg}')
    else:
        bot.send_message(message.chat.id, f'{msg} is incorrect')


@bot.message_handler(commands=['domains'])
def get_domains(message):
    msg = ''
    tmp = dbw.get_all_domains()
    for el in tmp:
        msg += f'{el[0]}. {el[1]} \n'
    msg = [msg[i:i + 3000] for i in range(0, len(msg), 3000)]
    for el in msg:
        bot.send_message(message.chat.id, f'ID | Domain\n {el}')


@bot.message_handler(commands=['last'])
def get_last_check(message):
    msg = 'Last status check:\n'
    with open('logs/status_last.txt', 'r') as f:
        msg += f.read()
    msg += '\n\nLast expiration date check:\n'
    with open('logs/exp_last.txt', 'r') as f:
        msg += f.read()
    msg += '\n\nLast existing tag check:\n'
    with open('logs/tag_last.txt', 'r') as f:
        msg += f.read()
    msg = [msg[i:i + 3000] for i in range(0, len(msg), 3000)]
    for el in msg:
        bot.send_message(message.chat.id, f'{el}')


# Run bot
bot.polling()
