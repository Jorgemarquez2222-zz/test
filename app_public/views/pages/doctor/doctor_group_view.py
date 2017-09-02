import logging
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from app_public.app.tools import get_json_from_jsonresponse
from app_public.views.api.doctor import ApiDoctorGroupInfo

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

"""
	The public view where users can see doctor's details
	and take appointments
"""


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ViewDoctorGroupView(TemplateView):
    template_name = "doctor/doctor_group_view.html"

    def get(self, request, *args, **kwargs):
        try:
            apiresp = ApiDoctorGroupInfo.as_view()(request)
            if apiresp.status_code != 200:
                return apiresp
            json = get_json_from_jsonresponse(apiresp)
            return render(request, self.template_name, {'doctor_group': json})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()
