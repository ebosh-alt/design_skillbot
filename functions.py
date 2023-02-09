from aiogram import types
from yookassa import Payment, Configuration

Configuration.account_id = '980889'
Configuration.secret_key = 'live_JB-sjh_-FPp_2Rl5QeX5Rlm6lwqarahXnk4YAbZCOnQ'


def create_pay(user_id: str, price: str) -> tuple:
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/design_ai_skillbot"

        },
        "capture": True,
        "description": user_id
    })

    return payment.confirmation.confirmation_url, payment.id


def create_keyboard(name_buttons: list, ) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=len(name_buttons), resize_keyboard=True, one_time_keyboard=True)
    array = []
    for name_button in name_buttons:
        array.append(
            types.KeyboardButton(text=name_button)
        )
    keyboard.add(*array)
    return keyboard


def inl_create_keyboard(buttons: list[list], ):
    keyboard = types.InlineKeyboardMarkup(row_width=len(buttons), resize_keyboard=True)
    array = []
    for button in buttons:
        if len(button) == 1:
            array.append(
                types.InlineKeyboardButton(text=button[0])
            )
        if len(button) == 2:
            array.append(
                types.InlineKeyboardButton(text=button[0], url=button[1])
            )
        if len(button) == 3:
            array.append(
                types.InlineKeyboardButton(text=button[0], url=button[1], callback_data="pay")
            )
    keyboard.add(*array)
    return keyboard


if __name__ == "__main__":
    create_pay("55", "29990.00")
