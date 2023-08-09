import asyncio

from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import AuthenticationForm
from firezone_api import FirezoneApi

fz_api = FirezoneApi()


class LoginView(LoginViewGeneric):
    form_class = AuthenticationForm
    template_name = "site_auth/login.html"
    next_page = reverse_lazy("site_auth:profile")


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("landing_page:index")


class ProfileView(TemplateView):
    template_name = "site_auth/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = "6a00408c-f3bb-41fa-a37e-4f25c76ecb26"  # Тестовый юзер
        devices = asyncio.run(fz_api.get_devices(user_id=user_id))
        context.update({"devices": devices})
        return context
