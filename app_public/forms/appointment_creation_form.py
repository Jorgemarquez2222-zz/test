from django.forms import ModelForm
from django.urls import reverse_lazy

from app_public.forms.widgets import TypeAheadWidget, SearchParameters
from app_public.forms.widgets.datetime_picker_widget import DateTimePickerWidget
from app_public.models import Appointment


class AppointmentCreationForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["work_place", "appointment_type", "start", "end"]
        widgets = \
            {
                "appointment_type": TypeAheadWidget(source_url_static=reverse_lazy('api_appointment_type'),
                                                    search_parameters=SearchParameters(['name'],
                                                    input_value_parser="""return data.data;""",
                                                    display_callback="""function (object) {return object.name;}""")),
                "start": DateTimePickerWidget(),
                "end": DateTimePickerWidget()
            }
