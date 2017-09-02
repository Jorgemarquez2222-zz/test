import random
from django import template
from app_public.app.model import is_doctor
from app_public.forms import LoginForm, PatientSubscribeForm, DoctorSubscribeForm

register = template.Library()

@register.simple_tag
def tag_is_doctor(user):
    if user.is_anonymous():
        return False
    return is_doctor(user)
    
@register.simple_tag
def tag_get_login_form():
    return LoginForm()
    
@register.simple_tag
def tag_get_displayed_image_url():
    return "/static/template/images/medical/bg/bg" + str(random.randint(1, 7)) + ".jpg"