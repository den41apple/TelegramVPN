"""
Работа с пользователями
"""
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from firezone_api.models import User
from telegram_bot.backend.db.actions import get_all_users
from telegram_bot.backend.utils import check_admin_access
from telegram_bot.dialogs.devices import Devices


class Users:
    user_details_prefix = "user_details_"

    def __init__(self):
        self._api = FirezoneApi()

    @check_admin_access
    async def list_users(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список пользователей
        """
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
            row.append(InlineKeyboardButton(button_text, callback_data=f"/{prefix}{user.id}"))
        if len(row) != 0:
            keyboard.add(*row)

    @check_admin_access
    async def user_details(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает информацию о пользователе
        """
        prefix = self.__class__.user_details_prefix
        fz_user_id = callback_query.data.replace(f"/{prefix}", "")
        user, devices = await asyncio.gather(
            self._api.get_user_by_id(user_id=fz_user_id), self._api.get_devices(user_id=fz_user_id)
        )
        # TODO: Отработать вариант с отсутствующим пользователем
        message_text = (
            f"ID: {user.id}\n"
            f"Email: {user.email}\n"
            f"Роль: {user.role}\n"
            f"Последний вход: {user.last_signed_in_at}\n"
            f"Создан: {user.inserted_at}\n"
            f"Обновлен: {user.updated_at}\n"
            f"Кол-во устройств: {len(devices)}\n"
            f"Последний вход с помощью: {user.last_signed_in_method}\n"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                f"Устройства [{len(devices)} шт]", callback_data=f"/{Devices.device_list_prefix}_<id:{fz_user_id}>"
            )
        )
        await callback_query.message.answer(message_text, reply_markup=keyboard)
