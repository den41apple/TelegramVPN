from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ProfileView,
    AddDeviceView,
    ConfirmDeleteDeviceView,
    DeleteDeviceView,
    NewDeviceInfoView,
DownloadConfigDeviceView,
)

app_name = "user_profile"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("add_device/", AddDeviceView.as_view(), name="add_device"),
    path(
        "new_device_info/",
        NewDeviceInfoView.as_view(),
        name="new_device_info",
    ),
    path(
        "download_config/",
        DownloadConfigDeviceView.as_view(),
        name="download_config",
    ),
    path(
        "<device_id>/confitm-delete/",
        ConfirmDeleteDeviceView.as_view(),
        name="confirm_delete_device",
    ),
    path(
        "<device_id>/delete/",
        DeleteDeviceView.as_view(),
        name="delete_device",
    ),

]
