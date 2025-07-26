from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🙎‍♂️ Профиль")],
        [KeyboardButton(text="📕 Категории")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню... 👇",
)

"""
Асинхронная функция, которая предлагает пользователю при регистрации вести его имея
или выбрать имя, которое зарегистрировано в телеграмме. 
"""
async def user_name(name):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=name)]],
        resize_keyboard=True,
        input_field_placeholder="Введите имя или оставьте такое же 👇",
    )
