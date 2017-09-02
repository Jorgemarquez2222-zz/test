from django import forms
from django.utils.translation import ugettext as _

from app_public.forms.fields import my_text_field, MyUniqueEmailField
from app_public.models.fields import my_phone_validator

class PatientSubscribeForm(forms.Form):
    email = MyUniqueEmailField()
    first_name = my_text_field(_("First name"), max_length=50)
    last_name = my_text_field(_("Last name"), max_length=50)
    phone = my_text_field(_("Phone"), max_length=20, min_length=5, required=False, validator=my_phone_validator)
    password = my_text_field(_("Password"), max_length=50, min_length=5, password=True)
    password_confirm = my_text_field(_("Confirm password"), max_length=50, min_length=5, password=True)

    def clean(self):
        self.cleaned_data = super(PatientSubscribeForm, self).clean()

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', forms.ValidationError(_("Passwords don't match")))

        return self.cleaned_data

class DoctorSubscribeForm(forms.Form):
    email = MyUniqueEmailField()
    first_name = my_text_field(_("First name"), max_length=50)
    last_name = my_text_field(_("Last name"), max_length=50)
    phone = my_text_field(_("Phone"), max_length=20, min_length=5, required=False, validator=my_phone_validator)
    password = my_text_field(_("Password"), max_length=50, min_length=5, password=True)
    password_confirm = my_text_field(_("Confirm password"), max_length=50, min_length=5, password=True)
    photo = forms.ImageField(required=False)

    def clean(self):
        self.cleaned_data = super(DoctorSubscribeForm, self).clean()

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            self.add_error('password_confirm', forms.ValidationError(_("Passwords don't match")))

        return self.cleaned_data