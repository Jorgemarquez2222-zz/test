import logging
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app_public.app.tools import get_json_from_jsonresponse
from app_public.views.api import ApiPatientInfo
from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ViewPatientView(TemplateView):
    template_name = "doctor/patient_view.html"

    def get(self, request, *args, **kwargs):
        try:
            apiresp = ApiPatientInfo.as_view()(request)
            if apiresp.status_code != 200:
                return apiresp
            json = get_json_from_jsonresponse(apiresp)
            return render(request, self.template_name, {'patient': json})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()