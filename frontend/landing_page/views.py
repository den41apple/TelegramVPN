from dataclasses import dataclass

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView
import config

@dataclass
class Product:
    """
    Продукт в карточке на главной странице
    """
    name: str
    period: str
    price: str
    description: str
    bg_class: str
    text_class: str = "text-white"


class LandingPageView(TemplateView):
    template_name = "landing_page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        containers_data = [
            Product(period="1 Месяц", price="300 ₽ ",
                    bg_class="bg-light", text_class="",
                    name="Базовый",
                    description=
"""- До 10 устройств
- 50 ГБ траффика - хватит на большинство задач
- Высокая скорость - гигабайтный канал
- Профессиональная и дружелюбная поддержка"""),
            Product(period="6 Месяцев", price="1 500 ₽",
                    name="Оптиум",
                    bg_class="bg-secondary",
                    description=
"""- 50 устройств
- Оптимальная цена
- 150 ГБ траффика - хватит на любые задачи
- Высокая скорость - гигабайтный канал
- Профессиональная и дружелюбная поддержка

"""),
            Product(period="12 Месяцев", price="2 400 ₽",
                    name="Бизнес",
                    bg_class="bg-dark",
                    description=
"""- Неограниченное количество устройств
- Не ограниченный траффик
- Высокая скорость - гигабайтный канал
- Профессиональная и дружелюбная поддержка
- Персональный менеджер отвечает в течении 3-х часов
- Скидки на продление
"""),
        ]
        context.update({"containers_data": containers_data})
        return context
