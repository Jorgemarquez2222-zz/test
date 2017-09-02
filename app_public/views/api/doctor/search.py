import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from app_public.app.search import search_doctor_by_name, search_doctor_by_distance, search_speciality_by_name, \
    search_group_by_name
from app_public.models import Speciality

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ApiSearch(TemplateView):
    def get(self, request, *args, **kwargs):
        try :
            logger.info("something")
            query_keys = request.GET.keys()
            # if group or/speciality is search another function should be called
            if 'search_text' in query_keys:
                search_text = request.GET['search_text']
                if 'group' in query_keys:
                    query = search_group_by_name(search_text)
                elif 'speciality' in query_keys:
                    query = search_speciality_by_name(search_text)
                else:
                    query = search_doctor_by_name(search_text)
            else:
                speciality_id = int(request.GET['speciality_id'])
                speciality = Speciality.objects.get(id=speciality_id)
                longitude = float(request.GET['longitude'])
                latitude = float(request.GET['latitude'])
                query = search_doctor_by_distance(longitude, latitude, speciality)

            data = [doc.get_info() for doc in query]
            return JsonResponse({'data': data})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        try:
            post_parameters = request.POST
            speciality_id = int(post_parameters['searchId'])
            speciality = Speciality.objects.get(id=speciality_id)
            longitude = float(post_parameters['longitude'])
            latitude = float(post_parameters['latitude'])
            query = search_doctor_by_distance(longitude, latitude, speciality)
            logger.info("Query result %s" % query)
            return query
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()