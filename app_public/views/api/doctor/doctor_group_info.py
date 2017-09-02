import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from app_public.models import DoctorGroup

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

"""
	Gets information for a doctor group from its id
	args
		- id : id of the doctor
"""


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ApiDoctorGroupInfo(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            doctor_id = int(request.GET['id'])
            doctor_group = DoctorGroup.objects.get(id=doctor_id)
            data = doctor_group.get_info()
            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()
