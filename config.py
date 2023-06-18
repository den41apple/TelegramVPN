"""
Переменные конфигурации
"""
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
WEBHOOK_TELEGRAM_HOST = env.str("WEBHOOK_TELEGRAM_HOST")
WEBHOOK_TELEGRAM_PATH = env.str("WEBHOOK_TELEGRAM_PATH", default='/path/to/api')
WEBAPP_HOST = env.str("WEBAPP_HOST", default="localhost")
APP_PORT = env.str("APP_PORT", default='8088')

# FIREZONE
FZ_HOST = env.str("FZ_HOST")
FZ_TOKEN = env.str("FZ_TOKEN")
