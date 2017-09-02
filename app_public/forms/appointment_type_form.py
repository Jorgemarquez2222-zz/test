from string import Template

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from app_public.forms.widgets.typeahead_widget import TypeAheadWidget, SearchParameters
from app_public.models import AppointmentType, Doctor
from app_public.forms.widgets import ColorPickerWidget


class AppointmentTypeForm(forms.ModelForm):
    appointment_type_id = forms.HiddenInput()

    class Meta:
        model = AppointmentType
        fields = ['name', 'duration', 'price', 'color', 'reservable', 'work_place', 'doctor']
        labels = {
            'name': _('Name'),
            'duration': _('Duration'),
            'price': _('Price'),
            'color': _('Color'),
            'reservable': _('Reservable'),
        }
        widgets = {
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': ColorPickerWidget(),
            'reservable': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'work_place': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
        }

    def __init__(self, doctor, work_place, *args, **kwargs):
        super(AppointmentTypeForm, self).__init__(*args, **kwargs)
        self.doctor = doctor
        self.fields['doctor'].initial = doctor
        self.work_place = work_place
        self.fields['work_place'].initial = work_place
        self.fields['name'].widget = TypeAheadWidget(source_url_static=reverse_lazy('api_appointment_type'),
                                              update_callback=self.generate_update_callback(),
                                              search_parameters=SearchParameters(['name'],
                                                input_value_parser="""return data.data;""",
                                                display_callback="""function (object) {return object.name;}"""),
                                              )

    def generate_update_callback(self) -> str:
        callback_template = Template("""
                    function (event, suggestion)
                    {
                        $$('#$durationId').val(suggestion.duration);
                        $$('#$priceId').val(suggestion.price);
                        $$('#$colorId').val(suggestion.color);
                        $$('#$reservableId').val(suggestion.reservable);
                    }
                        """)
        return callback_template.substitute(durationId=self.get_real_id("duration"),
                                            priceId=self.get_real_id("price"),
                                            colorId=self.get_real_id("color"),
                                            reservableId=self.get_real_id("reservable"))

    def get_real_id(self, field_name: str) -> str:
        assert field_name in self.fields
        return "id_%s-%s" % (self.prefix, field_name)

    def clean(self):
        cleaned_data = super(AppointmentTypeForm, self).clean()

        # Check if right doctor
        if not self.doctor == cleaned_data['doctor']:
            raise Exception("Trying to update AppointmentType with wrong Doctor")
        # Check if the workplace belongs to the doctor
        if not self.work_place == cleaned_data['work_place']:
            raise Exception("Trying to update AppointmentType with wrong WorkPlace")
        if not self.doctor.work_places.filter(pk=self.work_place.pk).exists():
            raise Exception("Trying to update AppointmentType with wrong WorkPlace")

        return cleaned_data
