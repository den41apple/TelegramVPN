"""
Регистрация обработчиков
"""
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from telegram_bot.dialogs import Main, Devices, Admin, Users


class HandlersRegistrator:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.main = Main()
        # Администрирование
        self.admin = Admin()
        # Пользователи
        self.users = Users()
        # Устройства
        self.devices = Devices()

        # Регистрация обработчиков
        self.register_handlers(dispatcher)

    def register_handlers(self, dp: Dispatcher):
        # Приветственное сообщение, привязка, и создание пользователя
        dp.register_message_handler(self.main.start, commands="start", state="*")

        #       УСТРОЙСТВА
        # Список устройств
        dp.register_callback_query_handler(
            self.devices.list_devices, text_contains=Devices.device_list_prefix, state="*",
        )
        # Создать новую конфигурацию, ввести имя
        dp.register_callback_query_handler(
            self.devices.get_name_for_new_device, text_contains="create_device", state="*"
        )
        # Создать новую конфигурацию
        dp.register_message_handler(self.devices.create_new_device, state="enter_device_name")
        # Информация об устройстве
        dp.register_callback_query_handler(
            self.devices.device_details, text_contains=Devices.device_details_prefix, state="*"
        )
        # Подтверждение удаления устройства
        dp.register_callback_query_handler(
            self.devices.device_confirm_delete, text_contains=Devices.device_confirm_delete_prefix, state="*"
        )
        # Удаление устройства
        dp.register_callback_query_handler(
            self.devices.delete_device, text_contains=Devices.delete_device_prefix, state="*"
        )

        #       АДМИНКА
        # Переход в режим админа
        dp.register_message_handler(self.admin.welcome, commands="admin", state="*")
        # Список пользователей
        dp.register_callback_query_handler(
            self.users.list_users, text_contains=Users.list_users_prefix, state="*"
        )
        # Информация о пользователе
        dp.register_callback_query_handler(
            self.users.user_details, text_contains=Users.user_details_prefix, state="*"
        )
        # Варианты привязки пользователя к Telegram аккаунту
        dp.register_callback_query_handler(
            self.users.link_telegram_account, text_contains=Users.link_tg_account_prefix, state="*"
        )
        # Варианты добавления пользователя
        dp.register_callback_query_handler(
            self.users.add_user, text_contains=Users.add_user_prefix, state="*"
        )
        # Генерация ссылки создания нового пользователя
        dp.register_callback_query_handler(
            self.users.generate_user_create_link,
            text_contains=Users.generate_user_create_link_prefix, state="*"
        )

