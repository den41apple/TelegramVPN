"""
Дополнение контекста
"""
from django.http import HttpRequest

import config


def add_context(request: HttpRequest) :
    print("ОТРАБОТАЛ")
    context = {"telegram_link": config.DJ_TELEGRAM_BOT_URL}
    return context
