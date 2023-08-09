from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.urls import reverse_lazy

from .forms import AuthenticationForm



class LoginView(LoginViewGeneric):
    form_class = AuthenticationForm
    template_name = "site_auth/login.html"
    next_page = reverse_lazy("user_profile:profile")


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("landing_page:index")


