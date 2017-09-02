import logging
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.permissions import test_is_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    Removes a work schedule used by a doctor
"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class ApiWorkscheduleRemove(TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            return HttpResponse()
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()