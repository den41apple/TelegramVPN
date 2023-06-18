"""
Регистрация обработчиков
"""


"""
Основной модуль с регистрацией хэндлеров
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
        dp.register_message_handler(dp.async_task(self.main.start), commands='start', state='*')
        # # Возврат SQL присланного ботом
        # dp.register_callback_query_handler(self.reports.view_sql, text_contains='return_sql',
        #                                    state='reports')