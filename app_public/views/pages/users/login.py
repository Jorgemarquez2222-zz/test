from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from app_public.forms import LoginForm

from app_public.views.api import apiLogin

@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewLogin(TemplateView):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('home'))
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('home'))

        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        apiresp = apiLogin(request)
        if apiresp.status_code == 200:
            return redirect(reverse('home'))

        form.add_error(None, _("Authentication failed"))
        return render(request, self.template_name, {'form': form})