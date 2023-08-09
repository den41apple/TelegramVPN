from django.urls import path
from django.views.generic import TemplateView

from .views import ProfileView

app_name = "user_profile"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
]
