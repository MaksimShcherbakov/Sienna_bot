from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from create_bot import engine


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)


class User_reg(Base):
    __tablename__ = 'user_reg'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    user_login: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()
    date_reg: Mapped[str] = mapped_column(DateTime)
    about: Mapped[str] = mapped_column(String(200))
    refer_id: Mapped[int] = mapped_column()


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="products")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
