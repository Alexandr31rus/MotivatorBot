import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.user import user

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")
