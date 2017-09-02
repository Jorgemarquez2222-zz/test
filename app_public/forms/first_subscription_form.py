from django import forms

from app_public.forms.fields import MyUniqueEmailField
from app_public.models import WorkPlace


class DoctorFirstSubscribeForm(forms.Form):
    first_name = forms.CharField(label='Nombre(s)', max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}
                                 ))
    last_name = forms.CharField(label='Apellidos', max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}
                                ))
    email = MyUniqueEmailField(label='Correo electrónico')
    email.widget = forms.TextInput(attrs={'class': 'form-control'})
    doctor_id = forms.CharField(label='CMP ó COP:', max_length=50,
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}
                                ))
    speciality = forms.CharField(label='Especialidades/Subespecialidades', max_length=100,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}
                                 ))
    formation = forms.CharField(label='Formación:', max_length=3000,
                                required=False,
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                        'rows': 6
                                    }
                                ))


class WorkPlaceCreationForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = ['name', 'phone', 'location', 'payment_method',
                  'ensurance', 'work_slots', 'description']
        labels = {
            'name': 'Nombre',
            'phone': 'Teléfono(s)',
            'location': 'Dirección',
            'payment_method': 'Tipo de pago',
            'ensurance': 'Seguro',
            'description': 'Descripción',
            'work_slots': 'Servicios y precios',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Consultorio privado, clínica y/o otros.'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número fijo y/o móvil'
            }),
            'location': forms.HiddenInput(),
            'payment_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Efectivo, tarjeta u otros'
            }),
            'ensurance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Afiliado con algún seguro?'
            }),
            'work_slots': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Primera consulta: S/50 , Examen de sangre: S/120  '
            }),
        }

    def __init__(self, *args, **kwargs):
        super(WorkPlaceCreationForm, self).__init__(*args, **kwargs)
        self.fields['location'].required = False
