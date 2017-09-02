import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from app_public.models import Doctor

from app_public.forms import DoctorSubscribeForm
from app_public.app.doctor.PhotoHandler import upload_photo

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
def apiSubscribeDoctor(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseBadRequest()

        form = DoctorSubscribeForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest(str(form.errors))

        is_save_valid, photo_id = upload_photo(request.FILES)
        if not is_save_valid:
            return HttpResponseBadRequest("Invalid photo upload")

        user = make_user(form.cleaned_data)
        doctor = Doctor(user=user,
                        phone=form.cleaned_data['phone'],
                        photo_id=photo_id)
        user.save()
        doctor.save()
        return HttpResponse()
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()
