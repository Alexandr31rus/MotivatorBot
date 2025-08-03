from aiogram import Bot

from app.database.requests import select_all_user
from app.database.requests import get_cards_by

# Функция выбора всех пользователй из БД и отправка им рандомной картинки из БД
async def task(bot: Bot):
    all_card = await get_cards_by()
    users = await select_all_user()
    results = users.fetchall()
    for result in results:
        await bot.send_photo(str(result), photo=all_card.image)