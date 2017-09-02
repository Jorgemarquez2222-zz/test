import logging
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.app.permissions import test_is_doctor
from app_public.app.model import get_doctor

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    Doctors agenda
"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_doctor), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewAgenda(TemplateView):
    template_name = "doctor/agenda.html"

    def get(self, request, *args, **kwargs):
        try:
            doctor = get_doctor(request.user)
            work_places = [wp.get_info(['id', 'name']) for wp in doctor.work_places.all()]

            return render(request, self.template_name, {'work_places': work_places})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try :
            return redirect(reverse('agenda_view'))
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()