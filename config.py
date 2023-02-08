import datetime
import logging

from aiogram import Bot, Dispatcher, executor

from Openai import OpenAi
from Users import Users

api_key = "5333826486:AAGWXbywv1pQ9AJ75d1zafg2xwBRBjtyYnI"
openai_api_key = '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'

bot = Bot(token=api_key)
dp = Dispatcher(bot)
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
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

WEBHOOK_HOST = "https://3bbf-109-252-118-243.ngrok.io"
WEBHOOK_PATH = f"/{api_key}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = "80"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

link_to_site = "https://www.skillbots.ru/design?utm_source=error_code_tg&utm_medium=tgbot"

link_to_bot = "https://t.me/test_for_flow_evg_bot"

user = users.get(686171972)
user.payment = False
users.update_info(user)