from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.tools import log_error, get_datetime_from_request
from app_public.app.model import get_patient_by_id, get_doctor
#from app_public.app.appointments import create_appointment
from app_public.app.permissions import test_is_doctor

"""
    The Doctor creates an appointment from his agenda
    args
        - patient_id
        - app_type_id : id of the appointment type
        - date : appointment beginning
"""
@login_required
@user_passes_test(test_is_doctor)
@require_http_methods(["POST"])
def apiAppointmentsMakeDoctor(request):
    try:
        doctor = get_doctor(request.user)
        patient = get_patient_by_id(request.POST['patient_id']) if request.POST['patient_id'] != '' else None
        app_type = doctor.appointment_types.get(id=request.POST['app_type_id']) if request.POST['app_type_id'] != '' else None
        start = get_datetime_from_request(request.POST['start'])
        end = get_datetime_from_request(request.POST['end']) if request.POST['end'] != '' else None
        name = request.POST['name'] if request.POST['name'] != '' else None

 #       create_appointment(doctor, patient, start, end=end, appointment_type=app_type, name=name)

        return HttpResponse()
    except Exception as e:
        log_error(str(e))
        return HttpResponseBadRequest()