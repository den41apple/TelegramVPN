"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


class Main:

    async def start(self, message: Message, state: FSMContext):
        """
        Приветственное сообщение
        """

        await message.answer("Привет")
