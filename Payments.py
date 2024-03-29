import time
from asyncio import run
from multiprocessing import Process

from yookassa import Payment

import functions
import texts
from Enum_classes import Flags
from config import users, bot


class Checking:
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

    def check_pay(self, key: str):
        try:
            res = Payment.find_one(key)
            if res.paid and res.status == "succeeded":

                return True
        except:
            return False

    async def work(self):
        list_user_id: list = users.get_keys()

        for user_id in list_user_id:
            try:
                user = users.get(user_id)

                if not user.payment and user.flag == Flags.Payment:
                    if self.check_pay(user.key_payment):
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

            except:
                pass

    def start_schedule(self):
        while True:
            run(self.work())
            time.sleep(30)




if __name__ == "__main__":
    checking = Checking()
    checking.check_pay("2b75d1d5-000f-5000-9000-15168f1fb17c")
    # checking.start_process(func=checking.start_schedule)
