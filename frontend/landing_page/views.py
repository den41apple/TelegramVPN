from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = "landing_page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        containers_data = [
            ("1 Месяц", "300"),
            ("6 Месяцев", "1 500"),
            ("1 год", "3 000"),
        ]
        context.update({"containers_data": containers_data})
        return context
