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
        keyboard.add(InlineKeyboardButton("Список пользователей", callback_data="/get_users"))
        keyboard.add(InlineKeyboardButton("Список Устройств", callback_data="/get_devices"))
        await message.answer("Привет", reply_markup=keyboard)


