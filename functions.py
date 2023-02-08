from aiogram import types
from bs4 import BeautifulSoup
from yookassa import Payment, Configuration

Configuration.account_id = '873492'
Configuration.secret_key = 'test_rFwIwdtgIwpyQgI555vYUd7u_Nd8p3u2A2h5o5diF0Q'


def create_pay(user_id: str, price: str) -> str:
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "embedded"
        },
        "capture": True,
        "description": user_id
    })
    return payment.confirmation.confirmation_token





def render_html(pay_token: str) -> str:
    with open("./templates/index.html", "r", encoding='utf-8') as inf:
        txt = inf.read()
    soup = BeautifulSoup(txt, 'html.parser')
    with open("./templates/index.js", "r", encoding='utf-8') as inf:
        txt = inf.read()
    new_soup = BeautifulSoup(txt, 'html.parser').prettify().split(" ")
    new_soup[15] = f"'{pay_token}',"
    txt = "<script>"
    for i in new_soup:
        txt += i + ' '
    txt += "\n  </script>"
    new_soup = BeautifulSoup(txt, 'html.parser')
    soup.body.append(new_soup)
    return soup.prettify()


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
    render_html(create_pay("55"))
