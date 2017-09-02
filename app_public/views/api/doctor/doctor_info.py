import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from app_public.models import Doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
	Gets information for a doctor from his id
	args
		- id : id of the doctor
"""


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ApiDoctorInfo(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            doctor_id = int(request.GET['id'])
            doctor = Doctor.objects.get(user__id=doctor_id)
            data = doctor.get_info()
            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()