from django import forms
from django.utils.translation import ugettext as _

from app_public.forms.fields import my_text_field
from app_public.models.fields import my_phone_validator


class PatientProfileForm(forms.Form):
    first_name = my_text_field(_("First name"), max_length=50)
    last_name = my_text_field(_("Last name"), max_length=50)
    phone = my_text_field(_("Phone"), max_length=20, min_length=5, required=False, validator=my_phone_validator)


class DoctorProfileForm(forms.Form):
    first_name = my_text_field(_("First name"), max_length=50)
    last_name = my_text_field(_("Last name"), max_length=50)
    description = my_text_field(_("Description"), max_length=3000, required=False, text_area=True)
    formation = my_text_field(_("Studies"), max_length=3000, required=False, text_area=True)
    languages = my_text_field(_("Languages"), max_length=1000, required=False, text_area=True)
    photo = forms.ImageField(required=False)
    phone = my_text_field(_("Phone"), max_length=20, min_length=5, required=False, validator=my_phone_validator)
