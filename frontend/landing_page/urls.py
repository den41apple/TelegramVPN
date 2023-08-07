from django.urls import path
from .views import landing_page_index

app_name = "landing_page"

urlpatterns = [path("", landing_page_index, name="index")]
