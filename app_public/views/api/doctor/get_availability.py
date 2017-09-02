import logging
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ApiGetAvailability(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse({})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()
