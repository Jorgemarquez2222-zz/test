from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from app_public.forms import PatientProfileForm

from app_public.app.tools import get_json_from_jsonresponse
from app_public.views.api import ApiProfilePatient
from app_public.app.permissions import test_is_patient

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(test_is_patient), name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewProfilePatient(TemplateView):
    template_name = "users/profile_patient.html"

    def get(self, request, *args, **kwargs):
        apiresp = ApiProfilePatient.as_view()(request)
        if apiresp.status_code != 200:
            return apiresp
        json = get_json_from_jsonresponse(apiresp)
        form = PatientProfileForm(json)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            apiresp = ApiProfilePatient.as_view()(request)
            if apiresp.status_code == 200:
                return redirect(reverse('profile_patient'))
            return apiresp
        return render(request, self.template_name, {'form': form})