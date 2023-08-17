"""
Администрирование
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from telegram_bot.backend.utils import check_admin_access
from telegram_bot.dialogs.users import Users



class Admin:
    def __init__(self):
        self._api = FirezoneApi()

    @check_admin_access
    async def welcome(self, message: Message, state: FSMContext):
        message_text = f"Приветствую в режиме администратора"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Список пользователей", callback_data=f"/list_users"))
        keyboard.add(InlineKeyboardButton("Добавить пользователя", callback_data=f"/{Users.add_user_prefix}"))
        await message.answer(message_text, reply_markup=keyboard)


