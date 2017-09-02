from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from app_public.views.api import apiSubscribePatient
from app_public.forms import PatientSubscribeForm


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewSubscribePatient(TemplateView):
    template_name = "users/subscribe_patient.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('home'))

        form = PatientSubscribeForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('home'))

        # Validate form or display again
        form = PatientSubscribeForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        apiresp = apiSubscribePatient(request)
        if apiresp.status_code == 200:
            return redirect(reverse('home'))

        return apiresp