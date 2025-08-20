from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_cards_by_category, get_cards_by

menu = ReplyKeyboardMarkup(
    keyboard=[
        # [KeyboardButton(text="🙎‍♂️ Профиль")],
        [KeyboardButton(text="💪 Мотивация")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню... 👇",
)

'''
Inline клавиатура рандомно выбирающая картинки из БД
'''
async def random_images():
    all_cards = await get_cards_by()
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Зарядиться мотивацией', callback_data=f"card_{all_cards.id}")]
            ])

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


"""
Создаём клавиатуру используя билдер. С помощью метода add добавляем кнопки в клавиатуру. 
С помощью функции get_categories достаем все категории, которые есть в БД и сохраняем в переменную all_categories. 
С помощью цикла for перебираем каждую по отдельности и добавляем кнопку с её названием. 
У каждой кнопки свой callback. Делаем префикс category_ и указываем id категории {category.id}. 
Возвращает клавиатуру с 2мя кнопками в одном ряду (adjust(2))
"""


async def categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await get_categories()
    for category in all_categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"category_{category.id}"
            )
        )
    return keyboard.adjust(2).as_markup()


"""
Создаём клавиатуру используя билдер.
Достали все карточки по определенной категории. 
С помощью цикла for перебираем каждую по отдельности. 
Создали кнопки Далее и Назад
"""


async def cards(category_id):
    keyboard = InlineKeyboardBuilder()
    all_cards = await get_cards_by_category(category_id)
    for card in all_cards:
        keyboard.row(
            InlineKeyboardButton(text=f"{card.name}", callback_data=f"card_{card.id}")
        )
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="categories"))
    return keyboard.as_markup()


async def back_to_categories(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад", callback_data=f"category_{category_id}"
                )
            ],
        ]
    )


admin_mod = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить ещё', callback_data='admin_mod')]
])