from django.urls import path
from django.views.generic import TemplateView

from .views import ProfileView, AddDeviceView

app_name = "user_profile"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("add_device/", AddDeviceView.as_view(), name="add_device"),
]
