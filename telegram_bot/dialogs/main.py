"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi


class Main:
    def __init__(self):
        self._api = FirezoneApi()

    async def start(self, message: Message, state: FSMContext):
        """
        Приветственное сообщение
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "Список пользователей", callback_data="/get_users"
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                "Список Устройств", callback_data="/get_devices"
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                "Создать новую конфигурацию устройства",
                callback_data="/create_device",
            )
        )
        await message.answer("Привет", reply_markup=keyboard)
