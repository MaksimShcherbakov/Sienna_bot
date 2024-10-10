import json

from datetime import datetime
from sqlalchemy import select, func, update, delete

from database.models import Category, Product, User_reg, Chat
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


async def get_dialog_history(user_id):
    async with async_session() as session:
        dialog_history_msg = []
        dialog_history = await session.scalars(select(Chat.message).where(Chat.user_id == user_id))

        for msg in dialog_history:
            message = json.loads(msg)  # Преобразуем строку в словарь
            dialog_history_msg.append(message)
        return dialog_history_msg


async def add_message_to_dialog_history(user_id, message, return_history=False):
    async with async_session() as session:
        new_chat = Chat(user_id=user_id, message=json.dumps(message))
        session.add(new_chat)
        await session.commit()
        if return_history:
            dialog_history = await get_dialog_history(user_id)
            return dialog_history


async def update_dialog_status(user_id, status):
    async with async_session() as session:
        update_status = (update(User_reg).where(User_reg.user_id == user_id).values(in_dialog=status))
        await session.execute(update_status)
        await session.commit()


async def clear_dialog(user_id: int, dialog_status: bool):
    async with async_session() as session:
        await session.execute(
            delete(Chat).where(Chat.user_id == user_id)
        )
        await update_dialog_status(user_id, dialog_status)
        await session.commit()


async def get_dialog_status(user_id: int):
    async with async_session() as session:
        stmt = select(User_reg.in_dialog).where(User_reg.user_id == user_id)
        result = await session.execute(stmt)
        user_data = result.scalar()
        return user_data
