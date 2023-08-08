from django.urls import path
from django.views.generic import TemplateView

from .views import LoginView

app_name = "site_auth"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("profile/",
         TemplateView.as_view(template_name="site_auth/profile.html"),
         name="profile")
]
