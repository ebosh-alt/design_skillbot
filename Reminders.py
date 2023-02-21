import time
from asyncio import run
import datetime
from multiprocessing import Process

import functions
import texts
from Enum_classes import Reminder
from config import users, bot, time_reminder_1, link_to_site, link_to_bot


class Reminders:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()

    @staticmethod
    async def work():
        list_user_id = users.get_keys()
        now_time = datetime.datetime.now().utcnow()

        for user_id in list_user_id:
            user = users.get(user_id)
            if not user.payment and user.count_reminder == 0 and user.time_transition_payment is not None:
                time_transition_payment = datetime.datetime.utcfromtimestamp(user.time_transition_payment)
                if (now_time - time_transition_payment) > time_reminder_1 and user.count_reminder == 0:
                    data = functions.create_pay(user_id=str(user_id),
                                                price=2990)
                    key = data[1]
                    link = data[0]
                    user.key_payment = key
                    await bot.send_message(chat_id=user_id,
                                           text=texts.text_for_reminder,
                                           reply_markup=functions.inl_create_keyboard(
                                               buttons=[["Оплатить 2990 руб.", link],
                                                        ["Узнать подробнее", link_to_site]]),
                                           parse_mode="Markdown",
                                           disable_web_page_preview=True)
                    user.count_reminder += 1
                users.update_info(user)

            if user.time_reminder is not None and not user.payment:
                time_reminder = datetime.datetime.utcfromtimestamp(user.time_reminder).timetuple()
                now_time_tuple = now_time.timetuple()
                if time_reminder.tm_mday == now_time_tuple.tm_mday and time_reminder.tm_hour == now_time_tuple.tm_hour \
                        and time_reminder.tm_min == now_time_tuple.tm_min:
                    if user.reminder == Reminder.first_reminder:
                        data = functions.create_pay(user_id=str(user_id),
                                                    price=2990)
                        key = data[1]
                        link = data[0]
                        user.key_payment = key
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_3,
                                               reply_markup=functions.inl_create_keyboard(
                                                   buttons=[["Оплатить 2990 руб.",
                                                             link]]))

                        time_rem = datetime.datetime(year=now_time_tuple.tm_year, month=now_time_tuple.tm_mon,
                                                     day=now_time_tuple.tm_mday, hour=14, minute=0, second=0)
                        time_rem += datetime.timedelta(days=1)
                        time_rem_tuple = time_rem.timetuple()
                        user.time_reminder = time.mktime(time_rem_tuple)
                        user.reminder = Reminder.second_reminder

                    elif user.reminder == Reminder.second_reminder:
                        data = functions.create_pay(user_id=str(user_id),
                                                    price=9990)
                        key = data[1]
                        link = data[0]
                        user.key_payment = key
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_4.format(username=user.username),
                                               reply_markup=functions.inl_create_keyboard(buttons=
                                                                                          [["Написать нам",link_to_bot],
                                                                                           ["Оплатить 9990 руб.", link]]
                                                                                          )
                                               )
                        time_rem = datetime.datetime(year=now_time_tuple.tm_year, month=now_time_tuple.tm_mon,
                                                     day=now_time_tuple.tm_mday, hour=15, minute=15, second=0)
                        time_rem += datetime.timedelta(days=2)
                        time_rem_tuple = time_rem.timetuple()
                        user.time_reminder = time.mktime(time_rem_tuple)
                        user.reminder = Reminder.third_reminder

                    elif user.reminder == Reminder.third_reminder:
                        data = functions.create_pay(user_id=str(user_id),
                                                    price=990)
                        key = data[1]
                        link = data[0]
                        user.key_payment = key
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_5.format(username=user.username),
                                               reply_markup=functions.inl_create_keyboard(buttons=
                                                                                          [["Оплатить 990 руб.",
                                                                                            link]]))
                        time_rem_tuple = datetime.datetime(year=now_time_tuple.tm_year, month=now_time_tuple.tm_mon,
                                                           day=now_time_tuple.tm_mday, hour=20, minute=30,
                                                           second=0).timetuple()

                        user.time_reminder = time.mktime(time_rem_tuple)
                        user.reminder = Reminder.fourth_reminder

                    elif user.reminder == Reminder.fourth_reminder:
                        data = functions.create_pay(user_id=str(user_id),
                                                    price=990)
                        key = data[1]
                        link = data[0]
                        user.key_payment = key
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_6,
                                               reply_markup=functions.inl_create_keyboard(buttons=
                                                                                          [["Оплатить 990 руб.",
                                                                                            link]]))
                        user.time_reminder = 0
                        user.reminder = Reminder.NONE
                    users.update_info(user)

    def start_schedule(self):
        while True:
            run(self.work())
            time.sleep(20)


if __name__ == "__main__":
    reminders = Reminders()
    reminders.start_process(func=reminders.start_schedule)
