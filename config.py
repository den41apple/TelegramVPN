"""
Переменные конфигурации
"""
from envparse import Env

env = Env()

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
WEBHOOK_TELEGRAM_HOST = env.str("WEBHOOK_TELEGRAM_HOST")
WEBHOOK_TELEGRAM_PATH = env.str("WEBHOOK_TELEGRAM_PATH", default='/path/to/api')
APP_PORT = env.str("APP_PORT", default='8088')
