import logging
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.forms import WorkPlaceForm, LocationForm, AppointmentTypeForm

from app_public.app.permissions import test_is_doctor
from app_public.app.model import get_doctor
from app_public.views import apiWorkPlace
from app_public.app.tools import get_json_from_jsonresponse

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewWorkPlace(TemplateView):
    template_name = "doctor/work_place.html"

    def get(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)
            work_place = None
            wp_id = None
            app_type_forms = None
            new_app_type_form = None
            if 'id' in request.GET.keys():
                wp_id = int(request.GET['id'])
                work_place = doctor.work_places.get(id=wp_id)

            work_place_form = WorkPlaceForm(doctor, instance=work_place, prefix='wp')
            location_form = LocationForm(instance= work_place.location if work_place else None, prefix='l')
            if not work_place is None:
                new_app_type_form = AppointmentTypeForm(doctor, work_place, prefix='n')
                app_type_forms = [AppointmentTypeForm(doctor, work_place, instance=appt, prefix=appt.id) for appt in work_place.appointment_types.all()]

            return render(request, self.template_name, {'wp_id': wp_id,
                                                        'work_place_form': work_place_form,
                                                        'location_form': location_form,
                                                        'new_app_type_form': new_app_type_form,
                                                        'app_type_forms': app_type_forms})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try :
            doctor = get_doctor(request.user)
            work_place = None
            location = None
            wp_id = None
            if 'id' in request.GET.keys():
                wp_id = int(request.GET['id'])
                work_place = doctor.work_places.get(id=wp_id)
                location = work_place.location

            work_place_form = WorkPlaceForm(doctor, request.POST, instance=work_place, prefix='wp')
            location_form = LocationForm(request.POST, instance=location, prefix='l')

            # Check forms
            if not work_place_form.is_valid():
                logger.warning("Form is not valid, %s" % work_place_form.errors)
                return render(request, self.template_name, {'wp_id': wp_id, 'work_place_form': work_place_form, 'location_form': location_form})
            if not location_form.is_valid():
                logger.warning("Form is not valid, %s" % location_form.errors)
                return render(request, self.template_name, {'wp_id': wp_id, 'work_place_form': work_place_form, 'location_form': location_form})

            apiresp = apiWorkPlace(request)
            if apiresp.status_code != 200:
                return apiresp
            json = get_json_from_jsonresponse(apiresp)

            return redirect(reverse('work_place_view') + "?id=" + str(json['id']))
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()