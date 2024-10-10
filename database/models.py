from typing import List
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, BIGINT
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

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    gender: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    user_login: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()
    date_reg: Mapped[str] = mapped_column(DateTime)
    about: Mapped[str] = mapped_column(String(200))
    refer_id: Mapped[int] = mapped_column()
    in_dialog: Mapped[bool] = mapped_column(Boolean, default=False)

    chats: Mapped[List['Chat']] = relationship('Chat', back_populates='user')


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


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_reg.user_id'))
    message: Mapped[str] = mapped_column()

    user: Mapped[User_reg] = relationship('User_reg', back_populates='chats')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
