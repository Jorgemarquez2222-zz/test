from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.tools import log_error, get_datetime_from_request
from app_public.app.model import get_doctor
#from app_public.app.workschedule import create_workschedule, parse_appointment_types
from app_public.app.permissions import test_is_doctor

"""
    Creates Doctor WorkSchedules to define when
    appointments can be taken with him
    GET
        Returns work schedules for the doctor
        args
            delete_id : If present, removes corresponding WS
    POST
        Create a new WS (recurrent by week from the start date)
        args
            start
            end
            recurrent
            recursion_end
"""
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ApiWorkschedule(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)

            l = []
            for work_schedule_group in doctor.work_schedule_groups.all():
                for work_schedule_slot in work_schedule_group.work_schedule_slots.all():
                    l.append(work_schedule_slot.get_info())

            return JsonResponse({'data': l})
        except Exception as e:
            log_error(str(e))
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)

            name = request.POST['name']
            start = get_datetime_from_request(request.POST['start'])
            end = get_datetime_from_request(request.POST['end'])
            recurrent = not request.POST.get('recurrent') is None
            appointment_types = parse_appointment_types(doctor, request.POST['appointment_types'])    
            recursion_end = get_datetime_from_request(request.POST['recursion_end']) if recurrent else None

            # Add appointment type
            wsg = create_workschedule(doctor, start, end, appointment_types=appointment_types, name=name, recurrent=recurrent, recursion_end=recursion_end)

            return HttpResponse()
        except Exception as e:
            log_error(str(e))
            raise e
            return HttpResponseBadRequest()