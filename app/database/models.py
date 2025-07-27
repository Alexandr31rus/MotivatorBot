from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(url="sqlite+aiosqlite:///database.db", echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Создание класса User, который является дочерним к классу Base
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25), nullable=True)


# Создание класса Category, который является дочерним к классу Base
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


# Создание класса Card, который является дочерним к классу Base
class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(256))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


# Создание функции init_models для создания базы данных с тремя таблицами
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
