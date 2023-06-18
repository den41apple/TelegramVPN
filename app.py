"""
Запуск приложения
"""
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

import config
from handlers import HandlersRegistrator


WEBHOOK_HOST = config.WEBHOOK_TELEGRAM_HOST
WEBHOOK_PATH = config.WEBHOOK_TELEGRAM_PATH
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=config.TELEGRAM_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=storage)
bot_app = HandlersRegistrator(bot=bot, dispatcher=dispatcher)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    user_commands = [types.BotCommand('start', 'Домой')]
    await dp.bot.set_my_commands(user_commands)


if __name__ == '__main__':
    start_webhook(dispatcher=dispatcher,
                  webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup,
                  on_shutdown=None,
                  skip_updates=True,
                  host=config.WEBAPP_HOST,
                  port=config.APP_PORT)
