from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.tools import log_error
from app_public.app.model import get_my_user
from app_public.app.appointments import remove_appointment
from app_public.app.permissions import test_is_patient_or_doctor

"""
    Cancels an appointment
    Removes the appointment from the database
    args
        app_id : The id of the appointment to remove
    Raises an exception if the appointment doest not
    involve the user
"""
@login_required
@user_passes_test(test_is_patient_or_doctor)
@require_http_methods(["POST"])
def apiAppointmentsCancel(request):
    try:
        appointment_id = request.POST['id']

        remove_appointment(appointment_id, get_my_user(request.user))
            
        return HttpResponse()
    except Exception as e:
        log_error(str(e))
        raise e
        return HttpResponseBadRequest()