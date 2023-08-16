"""
Полезные инструменты
"""
import random
from typing import Any, Callable

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import config


def generate_password(length: int = 20) -> str:
    """Генерирует случайный пароль"""
    digits = "1234567890"
    letters = "abcdefghijklmnopqrstuvwxyz"
    letters_upper = letters.upper()
    spec_symbols = "!@#$%^&*()-+~"
    all_symbols = digits + letters + letters_upper + spec_symbols
    password = [random.choice(all_symbols) for _ in range(length)]
    return "".join(password)


def check_admin_access(func: Callable) -> Callable:
    """
    Декоратор для проверки доступа
    к администрированию
    """

    async def wrapper(self,
                      callback_query_or_message: Message | CallbackQuery,
                      state: FSMContext) -> Any:
        if isinstance(callback_query_or_message, Message):
            message = callback_query_or_message
        elif isinstance(callback_query_or_message, CallbackQuery):
            message = callback_query_or_message.message
        else:
            raise ValueError(f'Неверный аргумент "callback_query_or_message"')
        chat_id = message.chat.id
        if chat_id not in config.TG_ADMINS:
            await message.answer("Этот раздел только для администраторов")
            return
        result = await func(self, callback_query_or_message, state)
        return result

    return wrapper
