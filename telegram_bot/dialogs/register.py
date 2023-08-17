"""
Регистрация пользователей
"""
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


from firezone_api import FirezoneApi
from firezone_api.exceptions import UserAlreadyExistsError
from telegram_bot.backend.db import async_session
from telegram_bot.backend.db.models import User
from telegram_bot.backend.utils import generate_password


class Register:
    def __init__(self):
        self._api = FirezoneApi()

    async def registration_options(self, callback_query: CallbackQuery, state: FSMContext):
        """Приветственное сообщение"""
        # TODO: Сделать с deep link
        message_text = """
        Для регистрации нажмите кнопку
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Зарегистрировать", callback_data="/register_user"))
        await callback_query.message.answer(message_text, reply_markup=keyboard)

    async def register_user(self, callback_query: CallbackQuery, state: FSMContext):
        """Регистрация пользователя"""
        tg_user = callback_query.from_user
        chat_id = callback_query.message.chat.id
        password = generate_password(length=20)
        email = f"{chat_id}@telegram_bot.ru"
        # Создание пользователя в Firezone
        try:
            fz_user = await self._api.create_user(email=email, password=password)
        except UserAlreadyExistsError as err:
            message_text = "Такой пользователь уже существует"
            await callback_query.message.answer(message_text)
            raise UserAlreadyExistsError(message_text)
        # Создание пользователя в БД Телеграм
        try:
            user = User(
                chat_id=chat_id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username,
                fz_user_id=fz_user.id,
                fz_is_admin=False,
                fz_email=email,
                fz_generated_password=password,
            )
            async with async_session() as session:
                async with session.begin():
                    session.add(user)
        except Exception as err:
            await self._api.delete_user(user_id=fz_user.id)
            raise err
        message_text = "Пользователь создан"
        await callback_query.message.answer(message_text)
