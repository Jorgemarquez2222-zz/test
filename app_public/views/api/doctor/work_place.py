import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest

from app_public.forms import WorkPlaceForm, LocationForm

from app_public.app.model import get_doctor
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@login_required
@user_passes_test(test_is_doctor)
@require_http_methods(["POST"])
def apiWorkPlace(request):
    try :
        doctor = get_doctor(request.user)
        work_place = None
        location = None

        if 'id' in request.GET.keys():
            wp_id = int(request.GET['id'])
            work_place = doctor.work_places.get(id=wp_id)
            location = work_place.location

        work_place_form = WorkPlaceForm(doctor, request.POST, instance=work_place, prefix='wp')
        location_form = LocationForm(request.POST, instance=location, prefix='l')

        # Check forms
        if not work_place_form.is_valid():
            logger.warning("Form is not valid, %s" % work_place_form.errors)
            return HttpResponseBadRequest()
        if not location_form.is_valid():
            logger.warning("Form is not valid, %s" % location_form.errors)
            return HttpResponseBadRequest()

        location = location_form.save()
        work_place_form.instance.location = location
        work_place = work_place_form.save()

        return JsonResponse({'id': work_place.id})
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()