"""
Регистрация обработчиков
"""
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes

from dialogs import Main


class HandlersRegistrator:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.main = Main()
        # Регистрация обработчиков
        self.register_handlers(dispatcher)

    def register_handlers(self, dp: Dispatcher):
        # Приветственное сообщение
        dp.register_message_handler(self.main.start, commands='start', state='*')
        # Показ пользователей
        dp.register_callback_query_handler(self.main.get_users, text_contains='get_users', state='*')
