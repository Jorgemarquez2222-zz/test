from django import forms

from .fields import MyEmailField, my_text_field


class LoginForm(forms.Form):
    email = MyEmailField(label='Correo electrónico: *')
    password = my_text_field('Contraseña: *', max_length=50, password=True)
