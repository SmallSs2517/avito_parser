from consts import COMMANDS
from telebot import TeleBot
import os
from dotenv import load_dotenv
from queue import SimpleQueue

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    bot = TeleBot(token=os.environ.get('BOT_TOKEN'))
except Exception as exc:
    print('Except in tg_bot, load_dotenv\n')
    print(exc)

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == 'get last':
        answer = get_last()
        print(f'it is answer - {answer}')
        bot.send_message(message.from_user.id, answer)
    elif message.text.lower() == 'get all avg':
        answer = get_all_avg()
        bot.send_message(message.from_user.id, answer)
    else:
        bot.send_message(message.from_user.id, COMMANDS['WELCOME'])


def get_last() -> str:
    db_in_queue.put(('gca', 1))
    return db_report_out_queue.get()

def get_all_avg() -> str:
    db_in_queue.put(('gaa', 1))
    return db_report_out_queue.get()

def bot_pooling(_db_in_queue: SimpleQueue, _db_report_out_queue: SimpleQueue):
    global db_in_queue, db_report_out_queue
    db_in_queue = _db_in_queue
    db_report_out_queue = _db_report_out_queue

    try:
        bot.infinity_polling(skip_pending=True, allowed_updates=['message'])
    except Exception as error:
        print(error)

