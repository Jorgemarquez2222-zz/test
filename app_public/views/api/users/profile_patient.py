import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.models import Patient

from app_public.app.model import get_patient
from app_public.forms import PatientProfileForm
from app_public.app.permissions import test_is_patient

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    GET
        Returns current user informations
    POST
        Sets current user info from a form
"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_patient), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ApiProfilePatient(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            user = get_patient(request.user)
            response = user.get_info(['first_name', 'last_name', 'phone', 'description'])
            return JsonResponse(response)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try:
            user = get_patient(request.user)

            if isinstance(user, Patient):
                form = PatientProfileForm(request.POST)

                if not form.is_valid():
                    raise Exception("Invalid form : " + str(form.errors))
            else:
                raise Exception('User type error.')

            user.user.first_name = form.cleaned_data['first_name']
            user.user.last_name = form.cleaned_data['last_name']
            user.phone = form.cleaned_data['phone']
            user.save()
            user.user.save()

            return HttpResponse()
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()