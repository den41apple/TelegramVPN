from django import forms


class DeviceForm(forms.Form):
    name = forms.CharField(label="Имя устройства")
    description = forms.CharField(label="Описание")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print(name, field)
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"
