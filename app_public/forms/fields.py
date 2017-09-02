from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


def my_text_field(label: str, initial=None, validator=None, max_length=100, min_length=0, required=True,
                  text_area=False,
                  password=False, place_holder: str = None):
    widget_class = forms.TextInput
    if text_area:
        widget_class = forms.Textarea
    elif password:
        widget_class = forms.PasswordInput

    field = forms.CharField(
        max_length=max_length,
        min_length=min_length,
        label=label,
        required=required,
        validators=[] if validator is None else [validator],
        initial="" if initial is None else initial,
        widget=widget_class(attrs={'placeholder': label if place_holder is None else place_holder}))

    return field


def build_text_field_typeahead(label: str, max_length: int) -> forms.CharField:
    field = my_text_field(label, max_length=max_length)
    field.widget.attrs["class"] = "typeahead"
    return field


class MyEmailField(forms.EmailField):
    def __init__(self, *args, **kwargs):
        super(MyEmailField, self).__init__(*args, **kwargs)


class MyUniqueEmailField(MyEmailField):
    def validate(self, value):
        super(MyUniqueEmailField, self).validate(value)
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError('Este correo ya está en uso')
