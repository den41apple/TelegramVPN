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
TG_UPDATE_MODE = env.str("TG_UPDATE_MODE", default="pooling")  # pooling | webhook
# Обязательные для веб-хука
TG_WEBHOOK_HOST = env.str("TG_WEBHOOK_HOST", default="").strip()
TG_WEBHOOK_PATH = env.str("TG_WEBHOOK_PATH", default="")
TG_WEBAPP_HOST = env.str("TG_WEBAPP_HOST", default="0.0.0.0")
TG_APP_PORT = env.str("TG_APP_PORT", default="8088")

TG_ADMINS: set = env.list("TG_ADMINS", default={}, postprocessor=lambda x: set(map(int, x)))  # Chat_ids администраторов
# Домен по умолчанию при регистрации пользователя
TG_DEFAULT_EMAIL_DOMAIN = env.str("TG_DEFAULT_EMAIL_DOMAIN", default="telegram_bot.ru")
# SQLAlchemy
TG_DB_NAME = env.str("TG_DB_NAME", default="bot")
TG_DB_ECHO = env.bool("TG_DB_ECHO", default=False)

# FIREZONE
FZ_HOST = env.str("FZ_HOST")
FZ_TOKEN = env.str("FZ_TOKEN")

########################################################################################################################
#                                                     DJANGO                                                           #
########################################################################################################################
DJ_SECRET_KEY = env.str("DJ_SECRET_KEY")
DJ_TELEGRAM_BOT_URL = env.str("DJ_TELEGRAM_BOT_URL")
DJ_DEBUG = env.bool("DJ_DEBUG", default=False)
DJ_DB_NAME = env.str("DJ_DB_NAME", default="site")
# url с портом разрешенные для генерации csrf токенов
DJ_CSRF_TRUSTED_ORIGINS = env.list("DJ_CSRF_TRUSTED_ORIGINS", default=[])

########################################################################################################################
#                                                      ОБЩЕЕ                                                           #
########################################################################################################################
POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
