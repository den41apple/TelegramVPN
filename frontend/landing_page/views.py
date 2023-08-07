from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def landing_page_index(request: HttpRequest) -> HttpResponse:
    return render(request, "landing_page/index.html")
