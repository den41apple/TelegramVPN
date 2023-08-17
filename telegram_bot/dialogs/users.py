"""
Работа с пользователями
"""
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

import config
from firezone_api import FirezoneApi
from firezone_api.models import User
from telegram_bot.backend.db import async_session
from telegram_bot.backend.db.models import DeeplinkAction
from telegram_bot.backend.db.actions import get_all_users, get_user_by_fz_user_id
from telegram_bot.backend.utils import (check_admin_access, generate_password, escaping,
                                        extract_id_from_callback_data)
from telegram_bot.dialogs.devices import Devices


class Users:
    list_users_prefix = "list_users"
    user_details_prefix = "user_details"
    add_user_prefix = "add_user_options"
    link_tg_account_prefix = "link_tg_account"
    generate_user_create_link_prefix = "generate_user_create_link"

    def __init__(self):
        self._api = FirezoneApi()

    @check_admin_access
    async def list_users(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список пользователей
        """
        # TODO обновлять e-mail в БД телеграма
        fz_users, users = await asyncio.gather(self._api.get_users(), get_all_users())
        telegram_fz_user_ids = {user.fz_user_id for user in users}
        answer = ""
        for i, user in enumerate(fz_users):
            # Помечем пользователей связанных с телеграм
            if user.id in telegram_fz_user_ids:
                answer += "🔗 "
            answer += f"Пользователь №{i + 1}:"
            answer += f"\nemail: {user.email}"
            answer += f"\nrole: {user.role}"
            answer += f"\ncreated at: {user.last_signed_in_at}"
            answer += "\n\n"
        keyboard = InlineKeyboardMarkup()
        self._fill_buttons_for_list_users(users=fz_users, keyboard=keyboard, telegram_fz_user_ids=telegram_fz_user_ids)
        keyboard.add(InlineKeyboardButton("Добавить пользователя", callback_data=f"/add_user_options"))
        await callback_query.message.answer(answer, reply_markup=keyboard)

    def _fill_buttons_for_list_users(
            self, users: list[User], keyboard: InlineKeyboardMarkup, telegram_fz_user_ids: set
    ):
        """Создает клавиатуру для списка пользователей"""
        prefix = self.__class__.user_details_prefix
        row = []
        devices_number_in_row = 2
        for i, user in enumerate(users):
            if len(row) == devices_number_in_row:
                if len(row) != 0:
                    keyboard.add(*row)
                row = []
            tg_related = ""
            if user.id in telegram_fz_user_ids:
                tg_related = "🔗"
            button_text = f"{tg_related} {i + 1}) {user.email}"
            row.append(InlineKeyboardButton(button_text, callback_data=f"/{prefix}_<id:{user.id}>"))
        if len(row) != 0:
            keyboard.add(*row)

    @check_admin_access
    async def user_details(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает информацию о пользователе
        """
        fz_user_id = extract_id_from_callback_data(callback_query)
        user, fz_user, devices = await asyncio.gather(
            get_user_by_fz_user_id(fz_user_id=fz_user_id),
            self._api.get_user_by_id(user_id=fz_user_id),
            self._api.get_devices(user_id=fz_user_id),
        )
        # TODO: Отработать вариант с отсутствующим пользователем
        message_text = (
            f"ID: {fz_user.id}\n"
            f"Email: {fz_user.email}\n"
            f"Роль: {fz_user.role}\n"
            f"Последний вход: {fz_user.last_signed_in_at}\n"
            f"Создан: {fz_user.inserted_at}\n"
            f"Обновлен: {fz_user.updated_at}\n"
            f"Кол-во устройств: {len(devices)}\n"
            f"Последний вход с помощью: {fz_user.last_signed_in_method}\n"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                f"Устройства [{len(devices)} шт]", callback_data=f"/{Devices.device_list_prefix}_<id:{fz_user_id}>"
            ),
        )
        if user is None:
            keyboard.add(
                InlineKeyboardButton(
                    f"🔗 Связать с телеграм-аккаунтом",
                    callback_data=f"/{Users.link_tg_account_prefix}_<id:{fz_user_id}>",
                )
            )
        await callback_query.message.answer(message_text, reply_markup=keyboard)

    @check_admin_access
    async def link_telegram_account(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Варианты добавления пользователя
        """
        fz_user_id = extract_id_from_callback_data(callback_query)
        link_param = generate_password(length=10, special_symbols=False)
        link = await get_start_link(link_param)
        deeplink_action = DeeplinkAction(id=link_param, to_link=True, fz_user_id=fz_user_id)
        async with async_session() as session:
            async with session.begin():
                session.add(deeplink_action)
        link = escaping(link)
        message_text = f"Ссылка для *привязки* пользователя Telegram \n*Нажмите, что бы скопировать* \n\n`{link}`"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(f"Назад", callback_data=f"/{Users.user_details_prefix}_<id:{fz_user_id}>"),
        )
        await callback_query.message.answer(message_text, reply_markup=keyboard, parse_mode="MarkdownV2")

    @check_admin_access
    async def add_user(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Варианты добавления пользователя
        """
        message_text = "Пользователь сможет создать учетную запись по сгенерированной ссылке"

        keyboard = InlineKeyboardMarkup()
        generate_link_prefix = self.__class__.generate_user_create_link_prefix
        list_users_prefix = self.__class__.list_users_prefix
        keyboard.add(InlineKeyboardButton(f"Сгенерировать ссылку", callback_data=f"/{generate_link_prefix}"))
        keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"/{list_users_prefix}"))
        await callback_query.message.answer(message_text, reply_markup=keyboard)

    @check_admin_access
    async def generate_user_create_link(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Генерация ссылки для нового пользователя
        """
        link_param = generate_password(length=10, special_symbols=False)
        deeplink_action = DeeplinkAction(id=link_param, to_create=True)
        async with async_session() as session:
            async with session.begin():
                session.add(deeplink_action)
        link = await get_start_link(link_param)
        link = escaping(link)
        message_text = f"Ссылка для *создания* пользователя Telegram \n*Нажмите, что бы скопировать* \n\n`{link}`"
        await callback_query.message.answer(message_text, parse_mode="MarkdownV2")
