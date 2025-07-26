import os
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter

load_dotenv()

ADMIN = os.getenv('ADMINS')


admin = Router()

class Admin(Filter):
    async def __call__(self, message: Message):
        return str(message.from_user.id) in ADMIN
    
@admin.message(Admin(), Command('admin'))
async def admin_panel(message: Message):
    await message.answer('Добро пожаловать в админ панель')

@admin.message(Admin(), F.photo)
async def get_photo(message: Message):
    await message.answer(message.photo[-1].file_id)