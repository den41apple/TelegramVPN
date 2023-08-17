"""
Действия с Базой данных
"""
from telegram_bot.backend.db import User, async_session
from sqlalchemy import select
from sqlalchemy.engine import Result


async def get_user_by_chat_id(chat_id: int) -> User | None:
    """
    Получает пользователя по chat_id
    """
    statement = select(User).where(User.chat_id == chat_id)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        user = result.one_or_none()
    return user


async def get_all_users() -> list[User]:
    """
    Запрашивает всех пользователей
    """
    statement = select(User)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        users = result.all()
    return users
