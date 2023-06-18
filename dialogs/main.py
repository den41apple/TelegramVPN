"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from firezone_api.models import User


class Main:

    def __init__(self):
        self._api = FirezoneApi()

    async def start(self, message: Message, state: FSMContext):
        """
        Приветственное сообщение
        """
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton("Показать пользователей", callback_data="/get_users")
        keyboard.add(button)
        await message.answer("Привет", reply_markup=keyboard)

    async def get_users(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список пользователей
        """
        users: list[User] = await self._api.get_users()
        answer = ""
        for i, user in enumerate(users):
            answer += f"Пользователь №{i+1}:"
            answer += f"\nemail: {user.email}"
            answer += f"\nrole: {user.role}"
            answer += f"\ncreated at: {user.last_signed_in_at}"
            answer += '\n\n'
        await callback_query.message.answer(answer)

