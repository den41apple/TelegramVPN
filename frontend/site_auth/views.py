from django.contrib.auth.views import LoginView as LoginViewGeneric
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import AuthenticationForm


class LoginView(LoginViewGeneric):
    form_class = AuthenticationForm
    template_name = "site_auth/login.html"
    next_page = reverse_lazy("site_auth:profile")
