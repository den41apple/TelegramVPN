"""
Переменные конфигурации
"""
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()

DJ_SECRET_KEY = env.str("DJ_SECRET_KEY")


