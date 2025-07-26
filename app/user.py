from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext


from app.database.requests import set_user, update_user, select_user
import app.keyboards as kb

user = Router()

"""
Проверка пользователя при нажатии команды /start. 
Если пользователя нет в БД, то предлагает ему зарегистрироваться. 
Если пользователь есть в БД, то выводит его имя и приветственное сообщение
"""


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer(
            "Добро пожаловать!👋\nПройдите процесс регистрации...\n\nВведите ваше имя или оставьте такое же 👇",
            reply_markup=await kb.user_name(message.from_user.first_name),
        )
        await state.set_state("reg_name")
    else:
        await message.answer(
            f"{await select_user(message.from_user.id)}, добро пожаловать!👋\n\nИспользуй кнопки ниже, чтобы войти в профиль или посмотреть картинки ⬇️",
            reply_markup=kb.menu,
        )


"""
Регистрация пользователя и добавление его имени в БД
"""


@user.message(StateFilter("reg_name"))
async def get_reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    data = await state.get_data()
    await update_user(message.from_user.id, data["name"])
    await message.answer(
        f"{await select_user(message.from_user.id)}, вы успешно зарегистрировались! ✅\n\nДобро пожаловать!👋",
        reply_markup=kb.menu,
    )
    await state.clear()


@user.message(F.text == "📕 Категории")
async def catalog(message: Message):
    await message.answer("Выберите категорию 👀", reply_markup=await kb.categories())


@user.callback_query(F.data.startswith("category_"))
async def cards(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split("_")[1]
    await callback.message.edit_text(
        "Выберите категорию", reply_markup=await kb.cards(category_id)
    )
