"""
Регистрация обработчиков
"""
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from telegram_bot.dialogs import Main, Devices, Users, Register


class HandlersRegistrator:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.main = Main()
        # Регистрация пользователей
        self.register = Register()
        # Пользователи
        self.users = Users()
        # Устройства
        self.devices = Devices()
        # Регистрация обработчиков
        self.register_handlers(dispatcher)

    def register_handlers(self, dp: Dispatcher):
        # Приветственное сообщение
        dp.register_message_handler(self.main.start, commands='start', state='*')
        #       РЕГИСТРАЦИЯ
        # Сообщение инструкция Регистрация пользователей
        dp.register_callback_query_handler(self.register.registration_options, text_contains='registration_options', state='*')
        # Создание пользователя
        dp.register_callback_query_handler(self.register.register_user, text_contains='register_user', state='*')

        # # Показ пользователей (АДМИН)
        # dp.register_callback_query_handler(self.users.get_users, text_contains='get_users', state='*')

        #       УСТРОЙСТВА
        # Показ устройств
        dp.register_callback_query_handler(self.devices.get_devices, text_contains=Devices.device_list_prefix, state='*')
        # Создать новую конфигурацию, ввести имя
        dp.register_callback_query_handler(self.devices.get_name_for_new_device,
                                           text_contains='create_device', state='*')
        # Создать новую конфигурацию
        dp.register_message_handler(self.devices.create_new_device, state='enter_device_name')
        # Информация об устройстве
        dp.register_callback_query_handler(self.devices.device_info,
                                           text_contains=Devices.device_info_prefix, state='*')
