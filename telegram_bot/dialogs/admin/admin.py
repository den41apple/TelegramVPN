"""
Администрирование
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from telegram_bot.backend.utils import check_admin_access


class Admin:
    def __init__(self):
        self._api = FirezoneApi()

    @check_admin_access
    async def welcome(self, message: Message, state: FSMContext):
        await state.set_state("admin")
        message_text = f"Приветствую в режиме администратора"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Список пользователей", callback_data="/list_users"))
        await message.answer(message_text, reply_markup=keyboard)


