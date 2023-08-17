"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import decode_payload

from firezone_api import FirezoneApi
from telegram_bot.backend.db.actions import get_user_by_chat_id
from telegram_bot.dialogs.devices import Devices


class Main:
    def __init__(self):
        self._api = FirezoneApi()

    async def start(self, message: Message, state: FSMContext):
        """
        Приветственное сообщение
        """
        deeplink_param = message.get_args()
        await self._clean_data(state)
        chat_id = message.chat.id
        keyboard = InlineKeyboardMarkup()
        user_registered = await self._check_user_registration(chat_id=chat_id)
        if deeplink_param != '':
            # TODO: Реализовать логику привязки аккаунта
            message_text = "Ваш телеграм аккаунт успешно привязан к существующему пользователю VPN"
            keyboard.add(InlineKeyboardButton("Список устройств", callback_data=f"/{Devices.device_list_prefix}"))
            keyboard.add(InlineKeyboardButton("Добавить устройство",
                                              callback_data="/create_device"))
        elif not user_registered:
            message_text = "Ты не зарегистрирован, необходимо пройти регистрацию"
            keyboard.add(InlineKeyboardButton("Регистрация пользователя", callback_data="/registration_options"))
        else:
            message_text = "Ты зарегистрирован, добро пожаловать"
            keyboard.add(InlineKeyboardButton("Список устройств", callback_data=f"/{Devices.device_list_prefix}"))
            keyboard.add(InlineKeyboardButton("Добавить устройство",
                                              callback_data="/create_device"))

        await message.answer(message_text, reply_markup=keyboard)



    async def _check_user_registration(self, chat_id: int) -> bool:
        """Проверяет регистрацию пользователя"""
        user = await get_user_by_chat_id(chat_id=chat_id)
        if user is None:
            return False
        return True

    async def _clean_data(self, state: FSMContext):
        """Правило очистки при переходе в начало"""
        data = await state.get_data()
        try:
            data.pop("user_id")
        except:
            pass
        await state.set_data(data)
