from django.contrib.auth.forms import (
    AuthenticationForm as AuthenticationFormGeneric,
)
from django import forms


class AuthenticationForm(AuthenticationFormGeneric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"
