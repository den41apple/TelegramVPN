from django.urls import path
from django.views.generic import TemplateView

from .views import LoginView, LogoutView
from user_profile.views import ProfileView

app_name = "site_auth"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
