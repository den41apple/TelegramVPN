import asyncio

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from firezone_api import FirezoneApi
from .forms import DeviceForm

fz_api = FirezoneApi()
user_id = "6a00408c-f3bb-41fa-a37e-4f25c76ecb26"  # Тестовый юзер


# Create your views here.
class ProfileView(TemplateView):
    template_name = "user_profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        devices = asyncio.run(fz_api.get_devices(user_id=user_id))
        context.update({"devices": devices})
        return context


class AddDeviceView(LoginRequiredMixin, FormView):
    template_name = "user_profile/add_device.html"
    form_class = DeviceForm
    success_url = reverse_lazy("user_profile:profile")

    def form_valid(self, form):
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        asyncio.run(fz_api.create_device(user_id=user_id,
                                         device_name=name,
                                         description=description))
        return super().form_valid(form)
