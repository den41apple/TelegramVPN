import asyncio

from django.shortcuts import render
from django.views.generic import TemplateView

from firezone_api import FirezoneApi

fz_api = FirezoneApi()

# Create your views here.
class ProfileView(TemplateView):
    template_name = "user_profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = "6a00408c-f3bb-41fa-a37e-4f25c76ecb26"  # Тестовый юзер
        devices = asyncio.run(fz_api.get_devices(user_id=user_id))
        context.update({"devices": devices})
        return context
