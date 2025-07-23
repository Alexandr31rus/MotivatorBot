from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext


from app.database.requests import set_user, update_user, select_user
import app.keyboards as kb

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer(
            "Добро пожаловать!👋\n\nВведите ваше имя",
            reply_markup=await kb.user_name(message.from_user.first_name),
        )
        await state.set_state("reg_name")
    else:

        await message.answer(
            f"{await select_user(message.from_user.id)}, добро пожаловать!👋",
            reply_markup=kb.menu,
        )


@user.message(StateFilter("reg_name"))
async def get_reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    data = await state.get_data()
    await update_user(message.from_user.id, data["name"])
    await message.answer(
        "✅ Вы успешно зарегистрировались!\n\nДобро пожаловать!👋", reply_markup=kb.menu
    )
    await state.clear()
