import asyncio

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from firezone_api import FirezoneApi
from .forms import AuthenticationForm, UserCreationForm
from .models import User

fz_api = FirezoneApi()

class LoginView(LoginViewGeneric):
    form_class = AuthenticationForm
    template_name = "site_auth/login.html"
    next_page = reverse_lazy("user_profile:profile")


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("landing_page:index")

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "site_auth/register.html"
    success_url = reverse_lazy("user_profile:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        user: AbstractUser = self.object
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        telegram_chat_id = form.cleaned_data.get("telegram_chat_id")
        fz_user = asyncio.run(fz_api.create_user(email=f"username@django.com",
                                                 password=password))
        my_user = User(user=user, telegram_chat_id=telegram_chat_id, firezone_id=fz_user.id)
        my_user.save()
        authenticate(self.request,
                     username=username,
                     password=password)
        login(self.request, user=user)
        return response

