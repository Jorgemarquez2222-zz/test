import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from app_public.models import Patient

from app_public.forms import PatientSubscribeForm

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


def make_user(cleaned_data):
    user = User.objects.create_user(
        username=cleaned_data['email'],
        email=cleaned_data['email'],
        password=cleaned_data['password'],
        first_name=cleaned_data['first_name'],
        last_name=cleaned_data['last_name'])
    return user


@require_http_methods(["POST"])
def apiSubscribePatient(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseBadRequest()
        
        form = PatientSubscribeForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        user = make_user(form.cleaned_data)
        patient = Patient(user=user)
        user.save()
        patient.save()

        return HttpResponse()
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()