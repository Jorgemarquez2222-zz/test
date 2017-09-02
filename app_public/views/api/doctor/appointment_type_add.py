import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.forms import AppointmentTypeForm
from app_public.app.model import get_doctor
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    Adds a new appointment type to a doctor
"""


@login_required
@user_passes_test(test_is_doctor)
@require_http_methods(["POST"])
def apiAppointmentTypeAdd(request):
    try:
        doctor = get_doctor(request.user)
        wpid = int(request.GET['work_place_id'])
        work_place = doctor.work_places.get(id=wpid)

        apptform = AppointmentTypeForm(doctor, work_place, request.POST, prefix='n')

        if not apptform.is_valid():
            logger.warning("Invalid AppointmentType modification : " + str(apptform.errors))
            return HttpResponseBadRequest()

        instance = apptform.save()
        data = instance.get_info(['id', 'name', 'duration', 'price', 'color'])

        return JsonResponse({'data': data})
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()