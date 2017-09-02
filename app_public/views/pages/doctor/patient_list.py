import logging
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ViewPatientList(TemplateView):
    template_name = "doctor/patient_list.html"

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()