"""
Полезные инструменты
"""
import random
import re
from typing import Any, Callable

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import config


def generate_password(length: int = 20, special_symbols: bool = True) -> str:
    """Генерирует случайный пароль"""
    digits = "1234567890"
    letters = "abcdefghijklmnopqrstuvwxyz"
    letters_upper = letters.upper()
    spec_symbols = "!@#$%^&*()-+~"
    all_symbols = digits + letters + letters_upper
    if special_symbols is True:
        all_symbols += spec_symbols
    password = [random.choice(all_symbols) for _ in range(length)]
    return "".join(password)


def check_admin_access(func: Callable) -> Callable:
    """
    Декоратор для проверки доступа
    к администрированию
    """

    async def wrapper(self, callback_query_or_message: Message | CallbackQuery, state: FSMContext) -> Any:
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


def extract_id_from_callback_data(callback_query: CallbackQuery) -> str | None:
    """Извлекает id из Callback data"""
    callback_data = callback_query.data
    pattern = RegexpPatterns.id_pattern
    ids = pattern.findall(callback_data)
    if len(ids) == 0:
        return None
    elif len(ids) == 1:
        return ids[0]
    else:
        raise ValueError("В Callback Data обнаружено несколько ID"
                         f'\nDATA :: "{callback_data}"')


def escaping(txt):
    """
    Экранирует проблемные символы для использования с Markdown
    """
    problem_symbols = ['.', '-', '?', '!', '(', ')',
                       "=", "_", "[", "]", "+"]
    for symb in problem_symbols:
        txt = txt.replace(symb, '\\' + symb)
    return txt


class RegexpPatterns:
    id_pattern = re.compile(r"<id:([\w\d\-]+)>")
