"""
Работа с пользователями
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from firezone_api.models import User
from telegram_bot.backend.utils import check_admin_access


class Users:
    user_info_prefix = "user_detail"

    def __init__(self):
        self._api = FirezoneApi()

    @check_admin_access
    async def list_users(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список пользователей
        """
        users: list[User] = await self._api.get_users()
        answer = ""
        for i, user in enumerate(users):
            answer += f"Пользователь №{i + 1}:"
            answer += f"\nemail: {user.email}"
            answer += f"\nrole: {user.role}"
            answer += f"\ncreated at: {user.last_signed_in_at}"
            answer += "\n\n"
        keyboard = InlineKeyboardMarkup()
        self._fill_buttons_for_list_users(users=users, keyboard=keyboard)
        await callback_query.message.answer(answer, reply_markup=keyboard)

    def _fill_buttons_for_list_users(self, users: list[User], keyboard: InlineKeyboardMarkup):
        """Создает клавиатуру для списка пользователей"""
        prefix = self.__class__.user_info_prefix
        row = []
        devices_number_in_row = 2
        for i, user in enumerate(users):
            if len(row) == devices_number_in_row:
                if len(row) != 0:
                    keyboard.add(*row)
                row = []
            button_text = f'{i + 1}) {user.email}'
            row.append(InlineKeyboardButton(button_text,
                                            callback_data=f"/{prefix}{user.id}"))

        if len(row) != 0:
            keyboard.add(*row)
