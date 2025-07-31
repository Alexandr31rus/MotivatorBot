import os
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter, StateFilter
from aiogram.fsm.context import FSMContext
from app.database.requests import add_card

import app.keyboards as kb

load_dotenv()

ADMIN = os.getenv('ADMINS')


admin = Router()

class Admin(Filter):
    async def __call__(self, message: Message):
        return str(message.from_user.id) in ADMIN
    
@admin.callback_query(F.data == 'admin_mod')   
@admin.message(Admin(), Command('god_mode'))
async def admin_panel(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state('add_img')
    if isinstance (event, Message):
        await event.answer('Добро пожаловать в админ панель\n\nДобавьте картинку')
    else:
        await event.answer('Вы вернулись в начало')
        await event.message.edit_text('Добро пожаловать в админ панель\n\nДобавьте картинку')


@admin.message(Admin(), F.photo, StateFilter('add_img'))
async def get_photo(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await state.set_state('add_category')
    await message.answer('Далее ...')
    await message.answer('Выберите категорию:\n1 - Мотиватор\n2 - Котики')
    # await message.answer(message.photo[-1].file_id)
    

@admin.message(Admin(), StateFilter('add_category'))
async def get_category(message: Message, state: FSMContext):
    
    await state.update_data(category_id=message.text)
    data = await state.get_data()
    # image = data.get('image')
    # category_id = data.get('category_id')
    await add_card(data['image'], data['category_id'])
    await message.answer('Картинка добавлена успешно', reply_markup=kb.admin_mod)
    await state.clear()