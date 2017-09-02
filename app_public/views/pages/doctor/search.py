import logging
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from app_public.app.tools import get_json_from_jsonresponse
from app_public.views.api.doctor.search import ApiSearch

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewSearch(TemplateView):
    template_name = "doctor/search.html"

    def get(self, request, *args, **kwargs):
        try:
            search_text = request.GET['search_text']
            apiresp = ApiSearch.as_view()(request)
            if apiresp.status_code != 200:
                return apiresp
            json = get_json_from_jsonresponse(apiresp)
            return render(request, self.template_name, {'search_text': search_text, 'results': json['data']})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        apiresp = ApiSearch.as_view()(request)
        return apiresp
