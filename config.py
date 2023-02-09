import datetime
import logging

from aiogram import Bot, Dispatcher, executor

from Enum_classes import Reminder
from Openai import OpenAi
from Users import Users

api_key = "5333826486:AAGWXbywv1pQ9AJ75d1zafg2xwBRBjtyYnI"
openai_api_key = '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'

bot = Bot(token=api_key)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
db_file_name = "db.db"

table_name = "users"
args = {
    'key': 'integer',
    'flag': 'integer',
    'payment': 'integer',
    'username': 'text',
    'time_transition_payment': 'integer',
    'count_reminder': 'integer',
    'key_payment': 'text',
    'time_reminder': 'integer',
    'reminder': 'integer'
}

users = Users(db_file_name=db_file_name, args=args, table_name=table_name)
time_reminder_1 = datetime.timedelta(hours=1)
time_reminder_2 = datetime.timedelta(hours=4)
OpenAI = OpenAi(openai_api_key)

code_for_payment = "SBND18244887"

introductory_part = "Ты Никки — робот, который учит дизайну и правилам дизайна. Тебе нужно ответить на вопрос твоего " \
                    "ученика. Он спрашивает:"

text_for_pay = "\n\nБолее подробно я отвечу после начала курса — для этого [активируйте полную версию](" \
               "https://www.skillbots.ru/design?utm_source=trial_tg&utm_medium=tgbot) 😊"

# WEBHOOK_HOST = "https://24ea-109-252-118-243.ngrok.io"
# WEBHOOK_PATH = f"/{api_key}"
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = "80"
# WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

link_to_site = "https://www.skillbots.ru/design?utm_source=error_code_tg&utm_medium=tgbot"

link_to_bot = "https://t.me/skillbots_support"

# user = users.get(686171972)
# user.payment = False
# user.count_reminder = 0
# user.key_payment = None
# user.time_transition_payment = 1675715160
# users.update_info(user)
# users_get = users.get_keys()
# for i in users_get:
#     user.reminder = Reminder.NONE
#     users.update_info(user)
