import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.model import get_doctor
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    Removes doctor's appointment type
    POST
        id
"""


@login_required
@user_passes_test(test_is_doctor)
@require_http_methods(["POST"])
def apiAppointmentTypeRemove(request):
    try:
        doctor = get_doctor(request.user)
        app_id = int(request.POST['id'])
        appt = doctor.appointment_types.get(id=app_id)

        appt.work_place.appointment_types.remove(appt)
        doctor.appointment_types.remove(appt)

        return HttpResponse()
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()