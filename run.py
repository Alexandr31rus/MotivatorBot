import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.user import user
from app.database.models import init_models

load_dotenv()

# Подключение логирования
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv("TOKEN"))

    dp = Dispatcher()
    dp.include_router(user)  # Регистрация роутеров
    dp.startup.register(startup)  # Регистрация функции startup
    dp.shutdown.register(shutdown)  # Регистрация функции shutdown

    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await init_models() # Создание таблиц БД
    logging.info("Bot started up...")


async def shutdown(dispatcher: Dispatcher):
    logging.info("bot shutting down ...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")
