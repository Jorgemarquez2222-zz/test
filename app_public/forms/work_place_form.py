from django import forms
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from app_public.forms.widgets.typeahead_widget import TypeAheadWidget, SearchParameters
from app_public.models import WorkPlace, Doctor
from app_public.forms.widgets import ColorPickerWidget


class WorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = ['name', 'doctor', 'location', 'phone', 'color', 'description']
        labels = {
            'name': _('Name'),
            'phone': _('Phone'),
            'description': _('Description'),
            'color': _('Color'),
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'color': ColorPickerWidget(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'doctor': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }

    def __init__(self, doctor, *args, **kwargs):
        super(WorkPlaceForm, self).__init__(*args, **kwargs)
        self.doctor = doctor
        self.fields['doctor'].initial = doctor
        self.fields['location'].required = False

    def clean(self):
        cleaned_data = super(WorkPlaceForm, self).clean()

        # Check if right doctor
        if not self.doctor == cleaned_data['doctor']:
            raise Exception("Trying to update AppointmentType with wrong Doctor")
        if not self.instance.pk is None and not self.doctor.work_places.filter(id=self.instance.id).exists():
            raise Exception("Trying to update foreign WorkPlace")

        return cleaned_data