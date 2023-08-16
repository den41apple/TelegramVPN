import asyncio
import warnings
import base64

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from firezone_api import FirezoneApi
from firezone_api.models import Device
from .forms import DeviceForm
from site_auth.models import User
from telegram_bot.backend.configuration_message import (
    prepare_config_file,
    prepare_configuration_qr_and_message,
)

fz_api = FirezoneApi()


# Create your views here.
class ProfileView(TemplateView):
    template_name = "user_profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        qs = User.objects.filter(user_id=current_user.pk).get()
        fz_user_id = qs.firezone_id
        devices = asyncio.run(fz_api.get_devices(user_id=fz_user_id))
        context.update({"devices": devices})
        return context


class AddDeviceView(LoginRequiredMixin, FormView):
    template_name = "user_profile/add_device.html"
    form_class = DeviceForm
    success_url = reverse_lazy("user_profile:new_device_info")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        current_user = self.request.user
        qs = User.objects.filter(user_id=current_user.pk).get()
        fz_user_id = qs.firezone_id
        device = asyncio.run(fz_api.create_device(user_id=fz_user_id, device_name=name, description=description))
        self.request.session["device"] = device.dict()
        return super().form_valid(form)


class NewDeviceInfoView(LoginRequiredMixin, TemplateView):
    """Конфигурация для нового устройства"""

    template_name = "user_profile/created_device_information.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.request.session["device"]
        device = Device(**device)
        # Генерация
        config_file_io, qr_image_file = prepare_configuration_qr_and_message(device=device)
        config_string = config_file_io.read()
        qr_bytes = qr_image_file.read()
        image_str = base64.b64encode(qr_bytes)
        image_b64 = image_str.decode("utf-8")
        context.update({"config_string": config_string, "device": device.dict(), "image_b64": image_b64})
        self.request.session["config_string"] = config_string
        return context


class DownloadConfigDeviceView(LoginRequiredMixin, TemplateView):
    """Загрузка файла конфигурации"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="configuration.conf"'},
        )
        config_string = self.request.session["config_string"]
        response.write(config_string)
        return response


class ConfirmDeleteDeviceView(LoginRequiredMixin, TemplateView):
    template_name = "user_profile/device_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = kwargs.get("device_id")
        if device_id is None:
            raise Exception("Не был получен device_id для удаления устройства")
        device = asyncio.run(fz_api.get_device_by_id(device_id=device_id))
        context.update({"device": device})
        return context


class DeleteDeviceView(ProfileView):
    def get_context_data(self, **kwargs):
        # Удаление устройства
        device_id = kwargs.get("device_id")
        if device_id is None:
            warnings.warn("Не был получен device_id для удаления устройства")
            return super().get_context_data(**kwargs)
        asyncio.run(fz_api.delete_device(device_id=device_id))
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        path = reverse_lazy("user_profile:profile")
        return HttpResponseRedirect(path)
