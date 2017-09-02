import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.Configuration import FILE_HANDLER
from app_public.app.doctor.PhotoHandler import upload_photo

from app_public.app.model import get_doctor
from app_public.forms import DoctorProfileForm
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    GET
        Returns current user informations
    POST
        Sets current user info from a form
"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ApiProfileDoctor(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)
            response = doctor.get_info(['first_name', 'last_name', 'phone', 'description', 'photo_url'])
            logger.info("Response is %s" % response)
            return JsonResponse(response)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)

            form = DoctorProfileForm(request.POST, request.FILES)

            if not form.is_valid():
                raise Exception("Invalid form : " + str(form.errors))

            is_save_valid, photo_id = upload_photo(request.FILES)
            if not is_save_valid:
                logger.error("Only one file should be uploaded")
                return HttpResponseBadRequest("Invalid photo upload")

            # Setting props
            doctor.description = form.cleaned_data['description']
            doctor.user.first_name = form.cleaned_data['first_name']
            doctor.user.last_name = form.cleaned_data['last_name']
            doctor.phone = form.cleaned_data['phone']
            
            # Updating photo if needed
            if len(photo_id) > 0:
                if len(doctor.photo_id) > 0:
                    logger.info("Deleting file with id %s" % doctor.photo_id)
                    FILE_HANDLER.delete(doctor.photo_id)
                doctor.photo_id = photo_id

            doctor.save()
            doctor.user.save()

            return HttpResponse()
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()