"""
Переменные конфигурации
"""
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()

########################################################################################################################
#                                                 ТЕЛЕГРАМ БОТ                                                         #
########################################################################################################################
TG_TOKEN = env.str("TG_TOKEN")
TG_WEBHOOK_HOST = env.str("TG_WEBHOOK_HOST")
TG_WEBHOOK_PATH = env.str("TG_WEBHOOK_PATH", default="/path/to/api")
TG_WEBAPP_HOST = env.str("TG_WEBAPP_HOST", default="localhost")
TG_APP_PORT = env.str("TG_APP_PORT", default="8088")
TG_ADMINS: set = env.list("TG_ADMINS", default={}, postprocessor=lambda x: set(map(int, x)))  # Chat_ids администраторов
# Домен по умолчанию при регистрации пользователя
TG_DEFAULT_EMAIL_DOMAIN = env.str("TG_DEFAULT_EMAIL_DOMAIN", default="telegram_bot.ru")
# SQLAlchemy
TG_DB_NAME = env.str("TG_DB_NAME")
TG_DB_ECHO = env.bool("TG_DB_ECHO", default=False)

# FIREZONE
FZ_HOST = env.str("FZ_HOST")
FZ_TOKEN = env.str("FZ_TOKEN")

########################################################################################################################
#                                                     DJANGO                                                           #
########################################################################################################################
DJ_SECRET_KEY = env.str("DJ_SECRET_KEY")
DJ_TELEGRAM_BOT_URL = env.str("DJ_TELEGRAM_BOT_URL")
DJ_DEBUG = env.bool("DJ_DEBUG", default=True)
DJ_DB_NAME = env.str("DJ_DB_NAME")

########################################################################################################################
#                                                      ОБЩЕЕ                                                           #
########################################################################################################################
POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
