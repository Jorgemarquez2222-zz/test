from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.tools import log_error, get_datetime_from_request
from app_public.app.model import get_doctor_by_id
from app_public.app.permissions import test_is_patient_or_doctor
#from app_public.app.appointments import is_available_appointment, create_appointment

"""
    A patient takes an appointment through the search
    args
        - doctor_id
        - app_type_id : id of the appointment type
        - date : appointment beginning
"""
@login_required
@user_passes_test(test_is_patient_or_doctor)
@require_http_methods(["POST"])
def apiAppointmentsMakePatient(request):
    try:
        doctor_id = request.POST['doctor_id']
        doctor = get_doctor_by_id(doctor_id)
        app_type_id = request.POST['app_type_id']
        app_type = doctor.appointment_types.get(id=app_type_id)
        date = get_datetime_from_request(request.POST['date'])
        patient = get_my_user(request.user)

        if not is_available_appointment(doctor, date, app_type):
            raise Exception('Trying to take an unavailable appointment')

        #create_appointment(doctor, my_user, app_type, date)

        return HttpResponse()
    except Exception as e:
        log_error(str(e))
        return HttpResponseBadRequest()