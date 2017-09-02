from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


my_phone_validator = RegexValidator(r"^[0-9\+\ \-]+$", "Solo números")
my_color_validator = RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", _("Wrong format."))


class MyPhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(MyPhoneField, self).__init__(
            max_length=20,
            blank=True,
            validators=[my_phone_validator])


class MyPriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        super(MyPriceField, self).__init__(
            default=0,
            max_digits=5,
            decimal_places=2)


class MyColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(MyColorField, self).__init__(
            max_length=20,
            default="#000000",
            validators=[my_color_validator])


class MyPhotoIdField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(MyPhotoIdField, self).__init__(
            max_length=50,
            blank=True)
