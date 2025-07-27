from app.database.models import async_session, User, Category, Card
from sqlalchemy import select, update
import random
from sqlalchemy.sql.expression import func

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


# Функция выбора всех категорий
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


# Функция выбора всех карточке по категории, которой выбрал пользователь
async def get_cards_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(
            select(Card).where(Card.category_id == category_id)
        )


# По id доставать определенную карточку
async def get_card(card_id):
    async with async_session() as session:
        return await session.scalar(select(Card).where(Card.id == card_id))

async def get_cards_by():
    async with async_session() as session:
        result = await session.scalars(select(Card))
        find = result.fetchall()
        return random.choice(find)

async def random_cards(card_id: int):
    async with async_session() as session:
        return await session.scalar(select(Card).where(Card.id == card_id))