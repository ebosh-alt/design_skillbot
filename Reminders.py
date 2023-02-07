import time
from asyncio import run
from datetime import datetime
from multiprocessing import Process

import texts
from config import users, time_reminder_2, bot, time_reminder_1


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
        now_time = datetime.now()
        
        for user_id in list_user_id:
            try:
                user = users.get(user_id)
                if not user.payment and user.count_reminder != 2:
                    time_transition_payment = datetime.utcfromtimestamp(user.time_transition_payment)
                    if (now_time - time_transition_payment) > time_reminder_1 and user.count_reminder == 0:
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_1,
                                               parse_mode="Markdwon")
                        user.count_reminder += 1
    
                    elif (now_time - time_transition_payment) > time_reminder_2 and user.count_reminder == 1:
                        await bot.send_message(chat_id=user_id,
                                               text=texts.text_for_reminder_2,
                                               parse_mode="Markdown")
                        user.count_reminder += 1
    
                    users.update_info(user)
            except:
                pass

    def start_schedule(self):
        while True:
            run(self.work())
            time.sleep(10)


if __name__ == "__main__":
    reminders = Reminders()
    reminders.start_process(func=reminders.start_schedule)
