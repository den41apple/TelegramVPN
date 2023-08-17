"""
Основной диалог при начале разговора
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import decode_payload

import config
from firezone_api import FirezoneApi
from firezone_api.exceptions import UserAlreadyExistsError
from telegram_bot.backend.db import async_session
from telegram_bot.backend.db.actions import get_user_by_chat_id, get_deeplink_action_by_id
from telegram_bot.backend.db.models import User, DeeplinkAction
from telegram_bot.backend.utils import generate_password
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
        if deeplink_param != "":
            deeplink_action = await get_deeplink_action_by_id(action_id=deeplink_param)
            if deeplink_action is None:
                return await message.answer("Передана неверная, либо устаревшая ссылка")
            if deeplink_action.to_create is True:
                message_text = await self._create_from_telegram_account(message=message,
                                                                        deeplink_action=deeplink_action)
            elif deeplink_action.to_link is True:
                # Привязка пользователя
                user = await get_user_by_chat_id(chat_id=chat_id)
                if user is not None:
                    message_text = "Вы уже связаны с существующим аккаунтом"
                else:
                    await self._link_telegram_account(message=message, deeplink_action=deeplink_action)
                    message_text = "Ваш телеграм аккаунт успешно привязан к существующему пользователю VPN"
            else:
                raise ValueError("Ни один из параметров по deeplink не удовлетворяет условиям")
            keyboard.add(InlineKeyboardButton("Список устройств", callback_data=f"/{Devices.device_list_prefix}"))
            keyboard.add(InlineKeyboardButton("Добавить устройство", callback_data="/create_device"))
        elif not user_registered:
            message_text = "Доступ только для зарегистрированных пользователей"
        else:
            message_text = "Ты зарегистрирован, добро пожаловать"
            keyboard.add(InlineKeyboardButton("Список устройств", callback_data=f"/{Devices.device_list_prefix}"))
            keyboard.add(InlineKeyboardButton("Добавить устройство", callback_data="/create_device"))

        await message.answer(message_text, reply_markup=keyboard)

    async def _link_telegram_account(self, message: Message, deeplink_action: DeeplinkAction):
        """Привязывает телеграм аккаунт"""
        tg_user = message.from_user
        chat_id = message.chat.id
        fz_user_id = deeplink_action.fz_user_id
        fz_user = await self._api.get_user_by_id(user_id=fz_user_id)
        user = User(
            chat_id=chat_id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            fz_user_id=fz_user_id,
            fz_is_admin=False,
            fz_email=fz_user.email,
            linked=True,
        )
        async with async_session() as session:
            async with session.begin():
                session.add(user)
                await session.delete(deeplink_action)

    async def _create_from_telegram_account(self, message: Message, deeplink_action: DeeplinkAction) -> str:
        """
        Создает пользователя в Firezone

        На основе аккаунта Telegram
        """
        tg_user = message.from_user
        chat_id = message.chat.id
        password = generate_password(length=20)
        email_domain = config.TG_DEFAULT_EMAIL_DOMAIN
        email = f"{chat_id}@{email_domain}"
        # Создание пользователя в Firezone
        try:
            fz_user = await self._api.create_user(email=email, password=password)
        except UserAlreadyExistsError as err:
            message_text = "Такой пользователь уже существует"
            await message.answer(message_text)
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
                    await session.delete(deeplink_action)
        except Exception as err:
            await self._api.delete_user(user_id=fz_user.id)
            raise err
        message_text = "Пользователь создан"
        return message_text

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
