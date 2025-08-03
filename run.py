import asyncio
import os
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.user import user
from app.admin import admin
from app.database.models import init_models
from app import tasks

load_dotenv()

# Подключение логирования
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv("TOKEN"))

    dp = Dispatcher()
    dp.include_routers(user, admin)  # Регистрация роутеров
    dp.startup.register(startup)  # Регистрация функции startup
    dp.shutdown.register(shutdown)  # Регистрация функции shutdown
    
    '''
        Ежедневная отправка сообщений в указанное время
    '''
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(tasks.task, trigger='cron', hour=9, minute=00, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(tasks.task, trigger='cron', hour=15, minute=00, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(tasks.task, trigger='cron', hour=21, minute=00, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.start()


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
