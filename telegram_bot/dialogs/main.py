"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.engine import Result

from firezone_api import FirezoneApi
from telegram_bot.backend.db import User, async_session


class Main:
    def __init__(self):
        self._api = FirezoneApi()

    async def start(self, message: Message, state: FSMContext):
        """
        Приветственное сообщение
        """
        chat_id = message.chat.id
        keyboard = InlineKeyboardMarkup()
        user_registered = await self._check_user_registration(chat_id=chat_id)
        if not user_registered:
            message_text = "Ты не зарегистрирован"
            keyboard.add(InlineKeyboardButton("Регистрация пользователя", callback_data="/registration_options"))
        else:
            message_text = "Ты зарегистрирован"
            # keyboard.add(InlineKeyboardButton("Список пользователей", callback_data="/get_users")) # ДЛЯ АДМИНА
            keyboard.add(InlineKeyboardButton("Список Устройств", callback_data="/get_devices"))
            keyboard.add(InlineKeyboardButton("Добавить конфигурацию устройства",
                                              callback_data="/create_device"))
        await message.answer(message_text, reply_markup=keyboard)

    async def _check_user_registration(self, chat_id: int) -> bool:
        """Проверяет регистрацию пользователя"""
        statement = select(User).where(User.chat_id == chat_id)
        async with async_session() as session:
            result: Result = await session.execute(statement)
            user = result.one_or_none()
        if user is None:
            return False
        return True
