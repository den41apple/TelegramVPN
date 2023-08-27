"""
Запуск приложения
"""
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook

import config
from telegram_bot.handlers import HandlersRegistrator

WEBHOOK_HOST = config.TG_WEBHOOK_HOST
WEBHOOK_PATH = config.TG_WEBHOOK_PATH
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=config.TG_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=storage)
bot_app = HandlersRegistrator(bot=bot, dispatcher=dispatcher)


async def on_startup(dp: Dispatcher):
    if config.TG_UPDATE_MODE == "webhook":
        await bot.set_webhook(WEBHOOK_URL)
    user_commands = [
        types.BotCommand("start", "Домой"),
        types.BotCommand("admin", "Админ. панель"),
    ]
    await dp.bot.set_my_commands(user_commands)


def main():
    if config.TG_UPDATE_MODE == "webhook":
        print("START WEBHOOK")
        kwargs = {}
        if config.TG_CERTIFICATE:
            kwargs.update(certificate=config.TG_CERTIFICATE)
        start_webhook(
            dispatcher=dispatcher,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=None,
            skip_updates=True,
            host=config.TG_WEBAPP_HOST,
            port=config.TG_APP_PORT,
            **kwargs,
        )
    else:
        print("START POOLING")
        start_polling(
            dispatcher=dispatcher,
            loop=None,
            skip_updates=True,
            reset_webhook=True,
            on_startup=on_startup,
            on_shutdown=None,
            timeout=20,
            relax=0.1,
            fast=True,
        )


if __name__ == "__main__":
    main()
