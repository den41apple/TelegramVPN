from django.contrib.auth.forms import (
    AuthenticationForm as AuthenticationFormGeneric,
    UsernameField,
    UserCreationForm as UserCreationFormGeneric,
)
from django import forms
from django.utils.translation import gettext_lazy

from .models import User


class AuthenticationForm(AuthenticationFormGeneric):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), label="Имя пользователя")
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": gettext_lazy("Введен не верный логин или пароль"),
        "inactive": gettext_lazy("Этот аккаунт неактивен"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control my-2"


class UserCreationForm(UserCreationFormGeneric):
    model = User
    telegram_chat_id = forms.CharField(label="Id чата в Telegram")

    class Meta(UserCreationFormGeneric.Meta):
        fields = "username", "telegram_chat_id"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя пользователя"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"
        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control my-2"
