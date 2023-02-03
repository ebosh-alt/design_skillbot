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
    'time_transition_payment': 'int',
    'count_reminder': 'int',
}
users = Users(db_file_name=db_file_name, args=args, table_name=table_name)
time_reminder_1 = datetime.timedelta(hours=1)
time_reminder_2 = datetime.timedelta(hours=4)

code_for_payment = "SBND18244887"

introductory_part = "Ты Никки — робот, который учит дизайну и правилам дизайна. Тебе нужно ответить на вопрос твоего " \
                    "ученика. Он спрашивает:"
OpenAI = OpenAi(openai_api_key)
