import time
from asyncio import run
from datetime import datetime
from multiprocessing import Process

import schedule

import functions
import texts
from config import users, time_reminder_2, bot, time_reminder_1, WEBHOOK_HOST, link_to_site


class Reminders:
    def __init__(self) -> None:
        self.p0 = Process()
        schedule.every().day.at("17:52").do(self.send_mes_1, mes=texts.text_for_reminder_3)

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()

    async def send_mes_1(self, mes: str):
        list_user_id: list = users.get_keys()
        for user_id in list_user_id:
            user = users.get(user_id)
            print(user_id)
            # if not user.payment:
            #     await bot.send_message(chat_id=user_id,
            #                            text=mes,
            #                            reply_markup=functions.inl_create_keyboard(buttons=
            #                                                                       [["Оплатить 2990 руб.",
            #                                                                         WEBHOOK_HOST + f"/pay?user_id={user_id}&price=2990.00"]]))

    @staticmethod
    async def work():
        list_user_id = users.get_keys()
        now_time = datetime.now()

        for user_id in list_user_id:

            user = users.get(user_id)
            if not user.payment and user.count_reminder != 1:
                time_transition_payment = datetime.utcfromtimestamp(user.time_transition_payment)
                if (now_time - time_transition_payment) > time_reminder_1 and user.count_reminder == 0:
                    await bot.send_message(chat_id=user_id,
                                           text=texts.text_for_reminder,
                                           reply_markup=functions.inl_create_keyboard(
                                               buttons=[["Оплатить 2990 руб.",
                                                         WEBHOOK_HOST + f"/pay?user_id={user_id}&price=2990.00"],
                                                        ["Узнать подробнее", link_to_site]]),
                                           parse_mode="Markdown",
                                           disable_web_page_preview=True)
                    user.count_reminder += 1
                users.update_info(user)

            if now_time.time().strftime("%H:%M") == "17:59":

                if not user.payment:
                    await bot.send_message(chat_id=user_id,
                                           text=texts.text_for_reminder_3,
                                           reply_markup=functions.inl_create_keyboard(buttons=
                                                                                      [["Оплатить 2990 руб.",
                                                                                        WEBHOOK_HOST + f"/pay?user_id={user_id}&price=2990.00"]]))


    def start_schedule(self):
        while True:
            schedule.run_pending()
            run(self.work())
            time.sleep(10)


if __name__ == "__main__":
    reminders = Reminders()
    reminders.start_process(func=reminders.start_schedule)
