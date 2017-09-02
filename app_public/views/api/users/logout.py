import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
	Logs out the current user
"""


@login_required
@require_http_methods(["POST"])
def apiLogout(request):
    try:
        logout(request)
        return HttpResponse()
    except Exception as e:
        logger.exception(e)
        return HttpResponseBadRequest()