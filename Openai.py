import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import openai_api_key

token = '5333826486:AAGWXbywv1pQ9AJ75d1zafg2xwBRBjtyYnI'
openai.api_key = openai_api_key
bot = Bot(token)
dp = Dispatcher(bot)

class OpenAI:
    def __init__(self):



@dp.message_handler()
async def send(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    await message.answer(response['choices'][0]['text'])


executor.start_polling(dp, skip_updates=True)
