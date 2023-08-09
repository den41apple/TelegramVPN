from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing_page.urls")),
    path("auth/", include("site_auth.urls")),
    path("profile/", include("user_profile.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
