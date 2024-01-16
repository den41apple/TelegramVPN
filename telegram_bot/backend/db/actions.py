"""
Действия с Базой данных
"""
from sqlalchemy import select
from sqlalchemy.engine import Result

from telegram_bot.backend.db import async_session
from telegram_bot.backend.db.models import User, DeeplinkAction


async def get_user_by_chat_id(chat_id: int) -> User | None:
    """
    Получает пользователя по chat_id
    """
    statement = select(User).where(User.chat_id == chat_id)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        user = result.one_or_none()
    return user


async def get_user_by_email(email: str) -> User | None:
    """
    Получает пользователя по email
    """
    statement = select(User).where(User.email == email)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        user = result.one_or_none()
    return user


async def get_user_by_fz_user_id(fz_user_id: str) -> User | None:
    """
    Получает пользователя по email
    """
    statement = select(User).where(User.fz_user_id == fz_user_id)
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


async def get_deeplink_action_by_id(action_id: str) -> DeeplinkAction:
    statement = select(DeeplinkAction).where(DeeplinkAction.id == action_id)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        deeplink_action = result.one_or_none()
    return deeplink_action
