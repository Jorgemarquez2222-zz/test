import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from app_public.models import AppointmentType

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    GET
        Returns public appointment types
"""


@require_http_methods(["GET"])
def apiAppointmentTypeGet(request):
        try:
            data = None
            fields = ['id', 'name', 'duration', 'price', 'color']

            if 'id' in request.GET.keys(): # Search for a specific appointment type
                apptid = int(request.GET['id'])
                query = AppointmentType.objects.get(id=apptid, validated=True)
                data = query.get_info(fields)
            else: # Search for appointment types by name
                query = AppointmentType.objects.filter(validated=True)
                data = [q.get_info(fields) for q in query]

            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()