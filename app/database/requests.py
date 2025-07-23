from app.database.models import async_session, User, Category, Card
from sqlalchemy import select, update


# Функция создания нового пользователя
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        return True if user.name else False

# Функция добавления имени пользователю
async def update_user(tg_id, name):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name))

        await session.commit()

# Функция выбора колонки name пользователя по его tg_id
async def select_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User.name).where(User.tg_id == tg_id))
