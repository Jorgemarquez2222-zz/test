from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods

from app_public.forms import LoginForm


"""
    Logs in the user
    POST
        email
        password
"""


@require_http_methods(["POST"])
def apiLogin(request):
    if request.user.is_authenticated():
        return HttpResponseBadRequest()

    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
    if user is None:
        return HttpResponseBadRequest()
        
    login(request, user)

    return HttpResponse()