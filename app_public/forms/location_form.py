from django import forms

from app_public.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['address', 'longitude', 'latitude']
        labels = {
            'address': 'Dirección'
        }
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Agregar una referencia si es necesario'
            }),
            'longitude': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
        }

    """
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = GoogleMapSearchWidget(
            latitude_id=self.get_latitude_id(),
            longitude_id=self.get_longitude_id())
    """

    def get_latitude_id(self) -> str:
        return 'id_%s-%s' % (self.prefix, 'latitude')

    def get_longitude_id(self) -> str:
        return 'id_%s-%s' % (self.prefix, 'longitude')
