from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from app_public.models import Appointment

from app_public.app.tools import log_error, get_datetime_from_request
from app_public.app.model import get_my_user
from app_public.app.permissions import test_is_patient_or_doctor

"""
    Returns the list of current users appointments
"""
@login_required
@user_passes_test(test_is_patient_or_doctor)
@require_http_methods(["GET"])
def apiAppointmentsGet(request):
    try:
        my_user = get_my_user(request.user)
        start_date = get_datetime_from_request(request.GET['start_date']) if 'start_date' in request.GET.keys() else None
        end_date = get_datetime_from_request(request.GET['end_date']) if 'end_date' in request.GET.keys() else None

        test = Q(patient=my_user) | Q(doctor=my_user)
        if not start_date is None:
            test = test & Q(start__gte=start_date)
        if not end_date is None:
            test = test & Q(end__lte=end_date)

        query = Appointment.objects.filter(test)

        appointments = [app.get_info(['id', 'name', 'doctor', 'patient', 'appointment_type', 'start', 'end']) for app in query]

        return JsonResponse({'data': appointments})
    except Exception as e:
        log_error(str(e))
        raise e
        return HttpResponseBadRequest()