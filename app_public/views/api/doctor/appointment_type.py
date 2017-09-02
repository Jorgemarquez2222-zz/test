import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from app_public.models import AppointmentType
from app_public.app.model import get_doctor
from app_public.forms import AppointmentTypeForm
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    GET
        Returns appointment types
    POST
        Updates an existing app type
"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ApiAppointmentType(TemplateView):
    fields = ['id', 'name', 'duration', 'price', 'color']

    def get(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)

            data = None

            if 'id' in request.GET.keys(): # Search for a specific appointment type
                apptid = int(request.GET['id'])
                query = AppointmentType.objects.get(Q(id=apptid) & (Q(doctor=doctor) | Q(validated=True)))
                data = query.get_info(self.fields)
            elif 'work_place_id' in request.GET.keys(): # Search for appts of a work place
                wpid = int(request.GET['work_place_id'])
                query = AppointmentType.objects.filter(work_place__id=wpid)
                data = [q.get_info(self.fields) for q in query]
            else: # Search for appointment types by name
                query = AppointmentType.objects.filter(Q(doctor=doctor) | Q(validated=True))
                data = [q.get_info(self.fields) for q in query]

            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)
            apptid = int(request.GET['id'])
            appointment_type = AppointmentType.objects.get(Q(id=apptid) & (Q(doctor=doctor) | Q(validated=True)))
            wpid = int(request.GET['work_place_id'])
            work_place = doctor.work_places.get(id=wpid)

            apptform = AppointmentTypeForm(doctor, work_place, request.POST, instance=appointment_type, prefix=apptid)

            if not apptform.is_valid():
                logger.warning("Invalid AppointmentType modification")
                return HttpResponseBadRequest()

            instance = apptform.save()
            data = instance.get_info(self.fields)

            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()