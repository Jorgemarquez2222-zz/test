import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from app_public.app.permissions import test_is_doctor
from app_public.app.search import search_patient_by_name

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@login_required
@user_passes_test(test_is_doctor)
@require_http_methods(["GET"])
def apiSearchPatient(request):
    try :
        search_text = request.GET['search_text']
        logger.info("kappa %s" % search_text)
        query = search_patient_by_name(search_text)

        data = [doc.get_info() for doc in query]

        return JsonResponse({'data': data})
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()