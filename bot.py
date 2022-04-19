import os
import telebot
import re
import datetime
import dateutil.parser as dparser
from DbHandler import DbHandler

API_KEY = os.getenv('API_KEY')
API_KEY = "5265235643:AAFHeaXEOg5Hqqp6XHOp91pUziLJ1ihKrY8"
bot = telebot.TeleBot(API_KEY)


class Request:
    def __init__(self):
        self.start_date = ''
        self.end_date = ''
        self.location: str = ''
        self.price: int = 0
        self.db_handler = DbHandler()

    def print_date_range(self):
        return f'{self.start_date.strftime("%d.%m.%y")}-{self.end_date.strftime("%d.%m.%y")}'

    def __str__(self):
        return f'מחפשים עבורכם דירה ב{self.location} בין התאריכים {self.print_date_range()} בתקציב של עד {self.price} ללילה...'

# 1. When?
# 2. Where?
# 3. How much?


@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, "אהלן! אני ג'וני, רובוט הסאבלטים הראשון בישראל!")
    bot.send_message(message.chat.id, "מה תאריכי הסאבלט שלכם?")
    bot.send_message(message.chat.id, "DD.MM.YYYY-DD.MM.YYYY")


def is_location(message):
    if 'גליל עליון' in message.text or 'ירושלים' in message.text or 'תל אביב' in message.text:
        return True
    else:
        return False


def is_price(message):
    if message.text.isnumeric():
        return True
    else:
        return False


def is_date(message):
    pattern = re.compile("\d+[.]\d+[.]\d+[-]\d+[.]\d+[.]\d+")
    if pattern.match(message.text):
        print('is_date=True')
        return True
    else:
        print('is_date=False')
        return False


@bot.message_handler(func=is_date)
def get_date_ask_for_location(message):
    start_date, end_date = message.text.split('-')
    request.start_date = dparser.parse(start_date, fuzzy=True, dayfirst=True).date()
    request.end_date = dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
    bot.send_message(message.chat.id, "איפה תרצו לחפש סאבלט?")
    bot.send_message(message.chat.id, "תל אביב \ ירושלים \ גליל עליון")


@bot.message_handler(func=is_location)
def get_location_ask_for_price(message):
    request.location = message.text
    bot.send_message(message.chat.id, "מה התקציב שלכם ללילה בשקלים?")


@bot.message_handler(func=is_price)
def get_price_and_search(self, message):
    request.price = int(message.text)
    bot.send_message(message.chat.id, str(request))
    bot.send_message(message.chat.id, 'your answer here!')
    # TODO [RS] : handle query here
    sublets = self.db_handler.bot_query(request.start_date, request.end_date, request.price, request.location)
    print (sublets)
    bot.send_message(message.chat.id, sublets)
    send_start_message(message)


request = Request()
bot.polling()

