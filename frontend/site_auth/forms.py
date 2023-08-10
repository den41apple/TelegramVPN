from django.contrib.auth.forms import (
    AuthenticationForm as AuthenticationFormGeneric,
)
from django import forms
from django.utils.translation import gettext_lazy


class AuthenticationForm(AuthenticationFormGeneric):
    error_messages = {
        "invalid_login": gettext_lazy("Введен не верный логин или пароль"),
        "inactive": gettext_lazy("Этот аккаунт неактивен"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"
