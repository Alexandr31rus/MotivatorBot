from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="➡ Категории")], [KeyboardButton(text="➡ Меню")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню... 👇",
)


async def user_name(name):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=name)]],
        resize_keyboard=True,
        input_field_placeholder="Введите имя или оставьте такое же 👇",
    )
