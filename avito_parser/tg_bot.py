from consts import COMMANDS
from telebot import TeleBot
import os
from dotenv import load_dotenv
from queue import SimpleQueue

load_dotenv()

bot = TeleBot(token=os.environ.get('BOT_TOKEN'))

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == 'get last':
        answer = get_last()
        bot.send_message(message.from_user.id, answer)


def get_last() -> str:
    db_in_queue.put(('gca', 1))
    return db_report_out_queue.get()


def bot_pooling(_db_in_queue: SimpleQueue, _db_report_out_queue: SimpleQueue):
    global db_in_queue, db_report_out_queue
    db_in_queue = _db_in_queue
    db_report_out_queue = _db_report_out_queue

    try:
        bot.infinity_polling(skip_pending=True, allowed_updates=['message'])
    except Exception as error:
        print(error)

