import utils.utils as ut

from datetime import datetime
from sqlalchemy import select, func

from database.models import Category, Product, User_reg
from create_bot import async_session


async def get_categories() -> Category:
    async with async_session() as session:
        result = await session.scalars(select(Category))
    return result


async def get_products(category_id) -> Product:
    async with async_session() as session:
        result = await session.scalars(select(Product).where(Product.category_id == category_id))
    return result


async def get_product(product_id) -> Product:
    async with async_session() as session:
        result = await session.scalar(select(Product).where(Product.id == product_id))
    return result


async def get_user_data(user_id) -> User_reg:
    async with async_session() as session:
        result = await session.scalar(select(User_reg).where(User_reg.user_id == user_id))
    return result


async def add_user(user_data):
    async with async_session() as session:
        current_time = datetime.now()
        new_user = User_reg(full_name=user_data['full_name'],
                            gender=user_data['gender'],
                            age=user_data['age'],
                            user_login=user_data['user_login'],
                            photo=user_data['photo'],
                            date_reg=current_time,
                            user_id=user_data['user_id'],
                            about=user_data['about'],
                            refer_id=user_data['refer_id'] if not None else None)
        session.add(new_user)
        await session.commit()
        print(f"Пользователь {new_user.full_name} успешно добавлен.")


async def get_all_users(count=True):
    async with async_session() as session:
        if count:
            result = await session.scalar(select(func.count(func.distinct(User_reg.user_id))))
        else:
            result = await session.scalar(select(User_reg))
    return result


async def check_code_exist(refer_code) -> bool:
    async with async_session() as session:
        result = await session.scalar(select(User_reg).where(User_reg.user_id == refer_code))
    return result is not None
