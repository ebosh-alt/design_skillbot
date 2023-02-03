from aiogram import types
import time

from Enum_classes import Flags
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
        user.username = message.from_user.username
    # print(texts.start_text.format(username=user.username))
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
        users.add(user_id)
        user = users.get(user_id)
        user.username = message.from_user.username
    users.update_info(user)


@dp.message_handler(lambda message: users.get(message.from_user.id).flag.name == "Payment",
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
                               parse_mode="Markdown"
                               )
        user.payment = True
        user.flag = Flags.NONE
        users.update_info(user)

    else:
        await bot.send_message(chat_id=user_id,
                               text=texts.not_successful_payment,
                               parse_mode="Markdown"
                               )


@dp.message_handler(lambda message: message.from_user.id in users, content_types=types.ContentTypes.TEXT)
async def main_hand(message: types.Message):
    user_id = message.from_user.id
    user = users.get(user_id)
    text = message.text
    if "никки," in text.lower():
        await message.reply("Минуту, сейчас я отвечу")
        response = await OpenAI.question(text=introductory_part + text)
        await bot.send_message(chat_id=user_id,
                               text=response,
                               parse_mode="Markdown",
                               # reply_markup=functions.create_keyboard(["Спасибо, Никки!"])

                               )

    # elif text == "Спасибо, Никки!":

    elif text == "Структура курса":
        await bot.send_message(chat_id=user_id,
                               text=texts.structure_course,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=keyboards.name_buttons_by_start[1::]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Сюжет курса":
        await bot.send_message(chat_id=user_id,
                               text=texts.plot_course,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=keyboards.name_buttons_by_start[0::2]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Хочу начать":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_for_payment,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown"
                               )
        user.flag = Flags.Payment
        user.time_transition_payment = time.mktime(message.date.timetuple())

    elif text == "Начать историю":
        await bot.send_message(chat_id=user_id,
                               text=texts.start_history_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я страшно занят", "Мне интересно, кто это"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Я страшно занят":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_scary,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Да иду я, ладно"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Мне интересно, кто это":
        await bot.send_message(chat_id=user_id,
                               text=texts.wonder_who_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Идти в холл"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Идти в холл" or text == "Да иду я, ладно":
        await bot.send_message(chat_id=user_id,
                               text=texts.text_1,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Слиться с ландшафтом и выжидать", "Заговорить первым"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Слиться с ландшафтом и выжидать":
        await bot.send_message(chat_id=user_id,
                               text=texts.landscape_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Заговорить первым"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Заговорить первым":
        await bot.send_message(chat_id=user_id,
                               text=texts.speak_first_text.format(username=user.username),
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кто ты?", "Вы меня с кем-то путаете"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Кто ты?" or text == "Вы меня с кем-то путаете":
        await bot.send_message(chat_id=user_id,
                               text=texts.who_you_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что за сюрприз?", "Что вам от меня надо?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Что за сюрприз?":
        await bot.send_message(chat_id=user_id,
                               text=texts.surprise_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что вам от меня надо?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Что вам от меня надо?":
        await bot.send_message(chat_id=user_id,
                               text=texts.you_want_me_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я все еще не понимаю🤨"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Я все еще не понимаю🤨":
        await bot.send_message(chat_id=user_id,
                               text=texts.dont_understand,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Что же за тыквы такие?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Что же за тыквы такие?":
        await bot.send_message(chat_id=user_id,
                               text=texts.pumpkins_these,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Но это же обычная тыква!"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Но это же обычная тыква!":
        await bot.send_message(chat_id=user_id,
                               text=texts.ordinary_pumpkin_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Как мне это сделать?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Как мне это сделать?":
        await bot.send_message(chat_id=user_id,
                               text=texts.how_do_this_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я готов(а)!", "А где же машина?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "А где же машина?":
        await bot.send_message(chat_id=user_id,
                               text=texts.car_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Я готов(а)!"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Я готов(а)!":
        await bot.send_message(chat_id=user_id,
                               text=texts.chapter_1,
                               parse_mode="Markdown"
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.i_ready_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Хорошо, я готов(а)"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Хорошо, я готов(а)":
        await bot.send_message(chat_id=user_id,
                               text=texts.good_i_ready_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Почему именно графический дизайн?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Почему именно графический дизайн?":
        await bot.send_message(chat_id=user_id,
                               text=texts.graphic_design_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["А это именно то, что нужно для нашей цели. Идем дальше!"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "А это именно то, что нужно для нашей цели. Идем дальше!":
        await bot.send_message(chat_id=user_id,
                               text=texts.our_goal_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Диджитал дизайн – что за зверь?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Диджитал дизайн – что за зверь?":
        await bot.send_photo(chat_id=user_id,
                             photo=texts.link_photo_1)
        await bot.send_message(chat_id=user_id,
                               text=texts.digital_design_text,
                               parse_mode="Markdown"
                               )
        await bot.send_message(chat_id=user_id,
                               text=texts.digital_design_2_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Кому все это нужно?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Кому все это нужно?":
        await bot.send_message(chat_id=user_id,
                               text=texts.who_needs_all_this_text,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown"
                               )

        await bot.send_message(chat_id=user_id,
                               text=texts.text_2,
                               reply_markup=functions.create_keyboard(
                                   name_buttons=["Какими навыками обладает диджитал дизайнер?"]
                               ),
                               parse_mode="Markdown"
                               )

    elif text == "Какими навыками обладает диджитал дизайнер?":
        await bot.send_message(chat_id=user_id,
                               text="texts.",
                               reply_markup=functions.create_keyboard(
                                   name_buttons=[]
                               ),
                               parse_mode="Markdown"
                               )

    # elif text == "":
    #     await bot.send_message(chat_id=user_id,
    #                            text=texts.,
    #                            reply_markup=functions.create_keyboard(
    #                                name_buttons=[]
    #                            ),
    #                            parse_mode="Markdown"
    #                            )
    #
    # elif text == "":
    #     await bot.send_message(chat_id=user_id,
    #                            text=texts.,
    #                            reply_markup=functions.create_keyboard(
    #                                name_buttons=[]
    #                            ),
    #                            parse_mode="Markdown"
    #                            )
    #
    # elif text == "":
    #     await bot.send_message(chat_id=user_id,
    #                            text=texts.,
    #                            reply_markup=functions.create_keyboard(
    #                                name_buttons=[]
    #                            ),
    #                            parse_mode="Markdown"
    #                            )
    #
    # elif text == "":
    #     pass
    users.update_info(user)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
