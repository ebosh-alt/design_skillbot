import datetime

from aiogram import types
import time

from Enum_classes import Flags, Reminder
from Payments import Checking
from Reminders import Reminders
from Users import User
from config import *
import keyboards
import texts
import functions


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    user = users.get(user_id)

    if not user:
        user = User(key=user_id)
        users.add(user)
        user = users.get(user_id)
        user.username = message.from_user.first_name

    user.flag = Flags.NONE
    await bot.send_message(chat_id=user_id,
                           text=texts.start_text.format(username=user.username),
                           reply_markup=functions.create_keyboard(name_buttons=keyboards.name_buttons_by_start,
                                                                  ),
                           disable_web_page_preview=False,
                           parse_mode="Markdown")
    users.update_info(user)


@dp.message_handler(lambda message: message.from_user.id not in users, content_types=types.ContentTypes.TEXT)
async def start(message: types.Message):
    user_id = message.from_user.id
    user = users.get(user_id)

    if not user:
        user = User(key=user_id)
        users.add(user)
        user = users.get(user_id)
        user.username = message.from_user.first_name
    user.flag = Flags.NONE
    users.update_info(user)


@dp.message_handler(lambda message: users.get(message.from_user.id).flag == Flags.Payment,
                    content_types=types.ContentTypes.TEXT)
async def check_payment(message: types.Message):
    user_id = message.from_id
    user = users.get(user_id)
    user_code = message.text
    if user_code == code_for_payment:
        await bot.send_message(chat_id=user_id,
                               text=texts.text_after_pay,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать историю"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.payment = True
        user.flag = Flags.NONE
        users.update_info(user)

    else:
        await bot.send_message(chat_id=user_id,
                               text=texts.not_successful_payment,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )


@dp.message_handler(lambda message: message.from_user.id in users, content_types=types.ContentTypes.TEXT)
async def main_hand(message: types.Message):
    user_id = message.from_user.id
    user = users.get(user_id)
    text = message.text
    if "никки," in text.lower():
        await message.reply("Загружаю твой вопрос... Подожди минутку")
        response = await OpenAI.question(text=introductory_part + text)
        if not user.payment:
            response += text_for_pay
        await bot.send_message(chat_id=user_id,
                               text=response,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Структура курса":
        await bot.send_message(chat_id=user_id,
                               text=texts.structure_course,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=keyboards.name_buttons_by_start[1::]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Сюжет курса":
        await bot.send_message(chat_id=user_id,
                               text=texts.plot_course,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=keyboards.name_buttons_by_start[0::2]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Хочу начать":
        data = functions.create_pay(user_id=str(user_id),
                                    price="2990.00")
        key = data[1]
        link = data[0]
        user.key_payment = key
        await bot.send_message(chat_id=user_id,
                               text=texts.text_for_payment,
                               reply_markup=functions.inl_create_keyboard(
                                   buttons=[["Оплатить 2990 руб.", link
                                             ]]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        now_time = message.date
        now_time_tuple = now_time.timetuple()
        user.flag = Flags.Payment
        user.time_transition_payment = time.mktime(now_time_tuple)
        user.reminder = Reminder.first_reminder
        if now_time_tuple.tm_hour >= 20 and now_time_tuple.tm_min >= 15:
            time_rem = datetime.datetime(year=now_time_tuple.tm_year, month=now_time_tuple.tm_mon,
                                         day=now_time_tuple.tm_mday, hour=19, minute=48, second=0)
            time_rem += datetime.timedelta(days=1)
            user.time_reminder = time.mktime(time_rem.timetuple())
        else:
            time_rem = datetime.datetime(year=now_time_tuple.tm_year, month=now_time_tuple.tm_mon,
                                         day=now_time_tuple.tm_mday, hour=19, minute=54, second=0)

            user.time_reminder = time.mktime(time_rem.timetuple())

    elif text == "Начать историю":
        await bot.send_message(chat_id=user_id,
                               text=texts.start_history_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я страшно занят", "Мне интересно, кто это"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я страшно занят":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_scary,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Да иду я, ладно"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Мне интересно, кто это":
        await bot.send_message(chat_id=user_id,
                               text=texts.wonder_who_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Идти в холл"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Идти в холл" or text == "Да иду я, ладно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_1,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Слиться с ландшафтом и выжидать", "Заговорить первым"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Слиться с ландшафтом и выжидать":
        await bot.send_message(chat_id=user_id,
                               text=texts.landscape_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Заговорить первым"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Заговорить первым":
        await bot.send_message(chat_id=user_id,
                               text=texts.speak_first_text.format(username=user.username),
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кто ты?", "Вы меня с кем-то путаете"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Кто ты?" or text == "Вы меня с кем-то путаете":
        await bot.send_message(chat_id=user_id,
                               text=texts.who_you_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что за сюрприз?", "Что вам от меня надо?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Что за сюрприз?":
        await bot.send_message(chat_id=user_id,
                               text=texts.surprise_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что вам от меня надо?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Что вам от меня надо?":
        await bot.send_message(chat_id=user_id,
                               text=texts.you_want_me_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я все еще не понимаю🤨"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я все еще не понимаю🤨":
        await bot.send_message(chat_id=user_id,
                               text=texts.dont_understand,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что же за тыквы такие?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Что же за тыквы такие?":
        await bot.send_message(chat_id=user_id,
                               text=texts.pumpkins_these,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Но это же обычная тыква!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Но это же обычная тыква!":
        await bot.send_message(chat_id=user_id,
                               text=texts.ordinary_pumpkin_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как мне это сделать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как мне это сделать?":
        await bot.send_message(chat_id=user_id,
                               text=texts.how_do_this_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я готов(а)!", "А где же машина?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "А где же машина?":
        await bot.send_message(chat_id=user_id,
                               text=texts.car_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я готов(а)!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    # переход к 1 главе
    elif text == "Я готов(а)!":
        await bot.send_message(chat_id=user_id,
                               text=texts.chapter_1,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.i_ready_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Хорошо, я готов(а)"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Хорошо, я готов(а)":
        await bot.send_message(chat_id=user_id,
                               text=texts.good_i_ready_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Почему именно графический дизайн?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Почему именно графический дизайн?":
        await bot.send_message(chat_id=user_id,
                               text=texts.graphic_design_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А это именно то, что нужно для нашей цели. Идем дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "А это именно то, что нужно для нашей цели. Идем дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.our_goal_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Диджитал дизайн – что за зверь?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Диджитал дизайн – что за зверь?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_1)
        await bot.send_message(chat_id=user_id,
                               text=texts.digital_design_text,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.digital_design_2_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кому все это нужно?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Кому все это нужно?":
        await bot.send_message(chat_id=user_id,
                               text=texts.who_needs_all_this_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_2,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Какими навыками обладает диджитал дизайнер?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Какими навыками обладает диджитал дизайнер?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_3,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_4,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А как же работает диджитал дизайнер?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "А как же работает диджитал дизайнер?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_5,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_6,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_7,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Где искать знания?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Где искать знания?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_8,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_2)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_3)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_4)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_9,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как все запомнить?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как все запомнить?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_10,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Готов(а)"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Test_1

    elif user.flag == Flags.Test_1:
        if text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_11,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_14,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_2

        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_12,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_13,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    elif user.flag == Flags.Test_2:
        if text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_17,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        # Переход к 2 главе
        elif text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_18,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_19,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Как тренировать насмотренность?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_15,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_16,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    elif text == "Как тренировать насмотренность?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_20,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_21,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Какие ресурсы посещать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Какие ресурсы посещать?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_22,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А еще?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "А еще?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_23,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_24,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как работать с материалом?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как работать с материалом?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_25,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как прокачать навыки?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как прокачать навыки?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_26,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что еще можно сделать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Что еще можно сделать?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_27,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи примеры мудбордов"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи примеры мудбордов":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_5)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_28,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Надеюсь это моя Феррари?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Надеюсь это моя Феррари?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_29,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_30,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_6,
                             caption=texts.text_31)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_32,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Да, все понятно"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Да, все понятно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_33,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Test_3

    # тест 3
    elif user.flag == Flags.Test_3:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_34,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_7,
                                 caption=texts.text_35,
                                 reply_markup=functions.create_keyboard(
                                     name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                 ),
                                 parse_mode="Markdown"
                                 )

        elif text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_36,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_4

        elif text == "Ответ 1":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_37,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_38,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
    # тест 4
    elif user.flag == Flags.Test_4:
        if text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_41,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        # Переход к 3 главе
        elif text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_42,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_43,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Скоро я тоже так смогу!", "А вдруг у меня не получится?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

        elif text == "Ответ 1":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_39,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_40,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    elif text == "Скоро я тоже так смогу!" or text == "А вдруг у меня не получится?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_44,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Погнали дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Погнали дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_45,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как же быть?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как же быть?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_46,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Записываю!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Записываю!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_8)
        await bot.send_message(chat_id=user_id,
                               text=texts.text_47,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Composition_1

    elif user.flag == Flags.Composition_1:
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_9)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_48,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Composition_2

    elif user.flag == Flags.Composition_2:
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_10)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_49,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Composition_3

    elif user.flag == Flags.Composition_3:
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_11)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_50,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Composition_4

    elif user.flag == Flags.Composition_4:
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_12)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_51,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, что дальше?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.NONE

    elif text == "Ок, что дальше?":

        await bot.send_message(chat_id=user_id,
                               text=texts.text_52,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_13)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_53,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Не терпится узнать о них"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Не терпится узнать о них":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_54,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_55,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Зачем нам сетки?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Зачем нам сетки?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_56,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как создать сетку?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как создать сетку?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_14)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_57,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Да, но хотелось бы попроще"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Да, но хотелось бы попроще":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_15)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_58,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как работать с сеткой?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как работать с сеткой?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_59,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Тыквы по клеточкам?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Тыквы по клеточкам?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_60,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_16,
                             caption=texts.text_61)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_17,
                             caption=texts.text_62)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_18,
                             caption=texts.text_63)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Погнали!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Погнали!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_65,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_66,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как это работает?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как это работает?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_19)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_67,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я думаю это будет тыква"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я думаю это будет тыква":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_68,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_20)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_69,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи пример"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи пример":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_21)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_70,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я все понял"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я все понял":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_72,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_73,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_74,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Давай подробнее!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Давай подробнее!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_75,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи пример!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи пример!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_22)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_76,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи пример с картинками"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи пример с картинками":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_23,
                             reply_markup=functions.create_keyboard(
                                 name_buttons=["Ок, я все понял"]
                             )
                             )

    elif text == "Ок, я все понял":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_78,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        user.flag = Flags.Test_5

    elif user.flag == Flags.Test_5:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_34,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_24,
                                 caption=texts.text_79,
                                 reply_markup=functions.create_keyboard(
                                     name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                 ),
                                 parse_mode="Markdown"
                                 )

        elif text == "Следующий вопрос":
            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_25,
                                 caption=texts.text_82,
                                 reply_markup=functions.create_keyboard(
                                     name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                 ),
                                 parse_mode="Markdown"
                                 )

            user.flag = Flags.Test_6

        elif text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_80,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_81,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    # тест 6
    elif user.flag == Flags.Test_6:
        if text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_85,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        # Переход к 4 главе
        elif text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_86,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_87,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Посмотреть, что там"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

        elif text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_83,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_84,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    elif text == "Посмотреть, что там":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_88,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Поехали!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Поехали!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_89,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Сложновато"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Сложновато":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_90,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_91,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_92,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, а дальше?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, а дальше?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_93,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_94,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_26)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_27)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cледующий стиль"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cледующий стиль":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_95,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_28)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_29)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cледующий стиль!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cледующий стиль!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_96,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_30)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_31)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cледyющий"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cледyющий":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_96,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_30)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_31)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cлeдующий"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cлeдующий":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_32)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_33)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cледующий"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cледующий":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_97,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_34)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_98,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Cлeдующий стиль"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Cлeдующий стиль":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_99,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text_100,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Расскажи подробнее"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Расскажи подробнее":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_35)
        await bot.send_message(chat_id=user_id,
                               text=texts.text_101,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, а еще!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, а еще!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_36)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_102,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oк, а еще!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Oк, а еще!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_36)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_103,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, а eщe!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, а eщe!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_104,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Понятно"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Понятно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_105,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_37)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_106,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, идем дальше"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, идем дальше":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_107,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Сложновато!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Сложновато!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_108,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_38)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_109,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я не в курсе!", "Давно в курсе!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я не в курсе!" or text == "Давно в курсе!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_110,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_39)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_111,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Для чего они?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Для чего они?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_112,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oк, идeм дальшe"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Oк, идeм дальшe":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_113,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_114,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Сложнoвато!", "Ок, идем дальшe"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Сложнoвато!" or text == "Ок, идем дальшe":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_115,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, постараюсь запомнить!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Ок, постараюсь запомнить!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_116,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Какие шрифты можно использовать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Какие шрифты можно использовать?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_40)

        await bot.send_message(chat_id=user_id,
                               text=texts.text_117,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, идем дaльше"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, идем дaльше":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_118,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, пoнятно"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, пoнятно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_119,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_41,
                             caption=texts.text__1)

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_42,
                             caption=texts.text__2)

        await bot.send_message(chat_id=user_id,
                               text=texts.text__3,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Спасибо, Никки!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Спасибо, Никки!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__4,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Test_7

    elif user.flag == Flags.Test_7:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_34,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_43,
                                 caption=texts.text__5,
                                 reply_markup=functions.create_keyboard(
                                     name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                 ),
                                 parse_mode="Markdown"
                                 )

        elif text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__8,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_8

        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__6,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__7,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
    # тест 4
    elif user.flag == Flags.Test_8:
        if text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__11,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        # Переход к 5 главе
        elif text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__12,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_43,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Как же выбрать цвет?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

        elif text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__9,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__10,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

    elif text == "Как же выбрать цвет?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__14,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_44)

        await bot.send_message(chat_id=user_id,
                               text=texts.text__15,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как работай задать цвет?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как работай задать цвет?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__16,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ого! Сложновато!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ого! Сложновато!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__17,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["я записываю!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "я записываю!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__18,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А в чем смысл?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "А в чем смысл?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__19,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Пoкажи примeр"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Пoкажи примeр":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__20,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ух ты!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Ух ты!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__21,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как этo работает?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как этo работает?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__22,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как создать палитру?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как создать палитру?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__23,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__24,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__25,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Похоже на игру!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Похоже на игру!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__26,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__27,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи пpимеp!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи пpимеp!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_45)
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_46)
        await bot.send_message(chat_id=user_id,
                               text=texts.text_77,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Давай"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Давай":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__28,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__29,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кaк это pаботает?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Кaк это pаботает?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__30,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_47)

        await bot.send_message(chat_id=user_id,
                               text=texts.text__31,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_48)

        await bot.send_message(chat_id=user_id,
                               text=texts.text__32,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_49)

        await bot.send_message(chat_id=user_id,
                               text=texts.text__33,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Настоящая магия!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Настоящая магия!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__34,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Хочу еще!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Хочу еще!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__35,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Отлично!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Отлично!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_50)
        await bot.send_message(chat_id=user_id,
                               text=texts.text__36,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Спасибо, очень интeрeсно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Спасибо, очень интeрeсно!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__37,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Test_9

    elif user.flag == Flags.Test_9:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text_34,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_51,
                                 caption=texts.text__38,
                                 reply_markup=functions.create_keyboard(
                                     name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                 ),
                                 parse_mode="Markdown"
                                 )

        elif text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__41,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_10

        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__39,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__40,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
    # тест 10
    elif user.flag == Flags.Test_10:
        if text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__44,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        # Переход к 6 главе
        elif text == "Готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__45,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=[]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__46,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Что это?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__42,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        else:
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__43,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
    elif text == "Что это?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__47,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Почему Figma?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Почему Figma?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__048,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Где взять?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Где взять?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__049,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подробнее, пожалуйста!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Подробнее, пожалуйста!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_052,
                             )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__050,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, идем дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, идем дальше!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_053,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__051,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подробнее, пожaлуйста!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Подробнее, пожaлуйста!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__052,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что такое слои?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Что такое слои?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_054,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__053,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как работать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как работать?":

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_055,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__054,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как изменить объекты?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Как изменить объекты?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__055,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, идeм дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, идeм дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__056,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_056,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__057,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["хочу ещё!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "хочу ещё!":

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_057,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__058,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["что еще можно делать?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "что еще можно делать?":

        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_058,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__059,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Понятнo!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Понятнo!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__060,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я записываю!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я записываю!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_059,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__061,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "понятно!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__062,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подробнее!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Подробнее!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__063,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_060,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__064,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oк, идем дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Oк, идем дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__065,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__066,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подрoбнeе!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Подрoбнeе!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__067,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__068,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["это все?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "это все?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__069,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__070,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__071,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oтлично!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Oтлично!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__072,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Спасибо, очень интересно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Спасибо, очень интересно!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__073,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать задание"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Начать задание":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__074,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__075,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Завершить задание"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Завершить задание":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__076,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я готoв(а)"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Я готoв(а)":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__077,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__078,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Не терпится узнать подробности"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Не терпится узнать подробности":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__079,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кaк это работает?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Кaк это работает?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__080,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подробнee!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Подробнee!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__081,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Понятнo"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Понятнo":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__082,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Пoнятно"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Пoнятно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__083,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oк, идем дальшe!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Oк, идем дальшe!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__084,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что для этого нужно?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Что для этого нужно?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__085,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи примeр!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Покажи примeр!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_061,
                             )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_062,
                             )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_063,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__086,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покaжи пример!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Покaжи пример!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_064,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__087,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Погнали"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Погнали":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__088,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Сколько всего!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Сколько всего!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__089,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_065,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__090,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Все понятно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Все понятно!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__091,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        user.flag = Flags.Test_11

    elif user.flag == Flags.Test_11:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__092,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__093,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__094,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_12

        elif text == "Ответ 1" or text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__095,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_12

    elif user.flag == Flags.Test_12:
        if text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__096,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 1":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__097,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_12

        elif text == "Ответ 3" or text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__098,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__099,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Я готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Я готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0100,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0101,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Что за этапы?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.NONE

    elif text == "Что за этапы?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0102,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, дальше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Ок, дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0103,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Пoнятнo"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Пoнятнo":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0104,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, дaльше!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Ок, дaльше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0105,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["записываю!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "записываю!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0106,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Это уже интересно!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    elif text == "Это уже интересно!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0107,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Пoкажи пример!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Пoкажи пример!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_066,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0108,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покaжи примeр!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
    elif text == "Покaжи примeр!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_067,
                             )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0109,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Все понятно!!!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
    elif text == "Все понятно!!!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0110,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Спaсибo, Никки!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
    elif text == "Спaсибo, Никки!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0111,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        user.flag = Flags.Test_13

    elif user.flag == Flags.Test_13:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0112,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0113,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0114,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_14
        elif text == "Ответ 1" or text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0115,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_14

    elif user.flag == Flags.Test_14:
        if text == "Следующий вопрос":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0116,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2", "Ответ 3"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 3":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0117,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 1" or text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0118,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0119,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Я готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Я готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0120,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0121,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Где же их искать?"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            user.flag = Flags.NONE

    elif text == "Где же их искать?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0122,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи примеры!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Покажи примеры!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0123,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["а платные?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "а платные?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0124,
                               parse_mode="Markdown",
                               disable_web_page_preview=True

                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0125,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как правильно подобрать фото?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True

                               )

    elif text == "Как правильно подобрать фото?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0126,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покaжи пpимeр!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True

                               )

    elif text == "Покaжи пpимeр!":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_068,
                             reply_markup=functions.create_keyboard(
                                 name_buttons=["Ок, все понятно"]
                             ),
                             parse_mode="Markdown"
                             )

    elif text == "Ок, все понятно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0127,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Отлично! Спасибо!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )

    elif text == "Отлично! Спасибо!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__0128,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Начать тест"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True
                               )
        user.flag = Flags.Test_15

    elif user.flag == Flags.Test_15:
        if text == "Начать тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0129,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_069,
                                 )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0130,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0131,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_16
        elif text == "Ответ 1":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0132,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Следующий вопрос"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            user.flag = Flags.Test_16

    elif user.flag == Flags.Test_16:
        if text == "Следующий вопрос":
            await bot.send_photo(chat_id=user_id,
                                 photo=texts.link_photo_070,
                                 )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0133,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Ответ 1", "Ответ 2"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 1":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0134,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
        elif text == "Ответ 2":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0135,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Завершить тест"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Завершить тест":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__0136,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Я готов(а)"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

        elif text == "Я готов(а)":
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__71,
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )
            await bot.send_message(chat_id=user_id,
                                   text=texts.text__72,
                                   reply_markup=functions.create_keyboard(
                                       name_buttons=["Зaписывaю!"]
                                   ),
                                   parse_mode="Markdown",
                                   disable_web_page_preview=True
                                   )

            user.flag = Flags.NONE

    elif text == "Зaписывaю!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__48,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Подробнeе!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Подробнeе!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__49,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Покажи пpимер"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Покажи пpимер":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__50,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Круто!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Круто!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__51,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Oк, идем дальше"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Oк, идем дальше":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__52,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А хард скилы?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "А хард скилы?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__53,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Ок, идем дальшe!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Ок, идем дальшe!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__54,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Чем хорош фриланс?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Чем хорош фриланс?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_52)
        await bot.send_message(chat_id=user_id,
                               text=texts.text__55,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Где искать работу фрилансеру?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Где искать работу фрилансеру?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__56,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Чем хорош найм?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Чем хорош найм?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_53)
        await bot.send_message(chat_id=user_id,
                               text=texts.text__55,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Где искать вакансии?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Где искать вакансии?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__57,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Пoнятнo!"]
                               ),
                               disable_web_page_preview=True
                               )

    elif text == "Пoнятнo!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__58,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Спaсибо, Никки!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True

                               )

    elif text == "Спaсибо, Никки!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__59,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__60,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text__61,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Отлично! Что дальше?"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Отлично! Что дальше?":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__62,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Завершить историю"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Завершить историю":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__63,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.text__64,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Никки!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Никки!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__65,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Привет Джессика!"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Привет Джессика!":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__66,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Отказаться от работы", "Начать работу"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Отказаться от работы":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__67,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Эпилог🏆"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Начать работу":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__68,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Эпилог🏆"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Эпилог🏆":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__69,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Завершить"]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )

    elif text == "Завершить":
        await bot.send_message(chat_id=user_id,
                               text=texts.text__70,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    else:
        await message.reply("Загружаю твой вопрос... Подожди минутку")
        response = await OpenAI.question(text=introductory_part + text)
        if not user.payment:
            response += text_for_pay
        await bot.send_message(chat_id=user_id,
                               text=response,
                               parse_mode="Markdown",
                               disable_web_page_preview=True,
                               )
    users.update_info(user)


if __name__ == "__main__":
    reminders = Reminders()
    reminders.start_process(func=reminders.start_schedule)

    checking = Checking()
    checking.start_process(func=checking.start_schedule)

    executor.start_polling(dispatcher=dp, skip_updates=True)
