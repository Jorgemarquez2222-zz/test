import logging

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from app_public.forms import DoctorFirstSubscribeForm, WorkPlaceCreationForm, LocationForm
from app_public.models import Doctor
from app_public.app.doctor.PhotoHandler import upload_photo
from app_public.app.tools import get_random_string

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


def do_render(request, template_name, form_subscribe, form_work_place_1, form_location_1,
              form_work_place_2, form_location_2, display_second=False):
    return render(request, template_name, {'form_subscribe': form_subscribe,
                                           'form_work_place_1': form_work_place_1,
                                           'form_location_1': form_location_1,
                                           'form_work_place_2': form_work_place_2,
                                           'form_location_2': form_location_2,
                                           'display_second': '1' if display_second else '0'})


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ViewSubscribeDoctor(TemplateView):
    template_name = "users/subscribe_doctor.html"

    def get(self, request, *args, **kwargs):
        form_subscribe = DoctorFirstSubscribeForm(prefix='s')
        form_work_place_1 = WorkPlaceCreationForm(prefix='w1')
        form_location_1 = LocationForm(prefix='l1')
        form_work_place_2 = WorkPlaceCreationForm(prefix='w2')
        form_location_2 = LocationForm(prefix='l2')

        return do_render(request, self.template_name, form_subscribe,
                         form_work_place_1, form_location_1, form_work_place_2,
                         form_location_2)

    def post(self, request, *args, **kwargs):
        try:
            nb_workplaces = int(request.POST['nb_workplaces'] if 'nb_workplaces' in request.POST.keys() else '1')

            form_subscribe = DoctorFirstSubscribeForm(request.POST, request.FILES, prefix='s')
            form_work_place_1 = WorkPlaceCreationForm(request.POST, prefix='w1')
            form_location_1 = LocationForm(request.POST, prefix='l1')
            form_work_place_2 = WorkPlaceCreationForm(request.POST, prefix='w2')
            form_location_2 = LocationForm(request.POST, prefix='l2')
            
            if not form_subscribe.is_valid():
                return do_render(request, self.template_name, form_subscribe, form_work_place_1, form_location_1, form_work_place_2, form_location_2)
            if not form_work_place_1.is_valid() or not form_location_1.is_valid():
                if nb_workplaces >= 2:
                    return do_render(request, self.template_name, form_subscribe, form_work_place_1, form_location_1, form_work_place_2, form_location_2, display_second=True)
                else:
                    return do_render(request, self.template_name, form_subscribe, form_work_place_1, form_location_1, form_work_place_2, form_location_2)
            if nb_workplaces >= 2 and (not form_work_place_2.is_valid() or not form_location_2.is_valid()):
                return do_render(request, self.template_name, form_subscribe, form_work_place_1, form_location_1, form_work_place_2, form_location_2, display_second=True)

            is_save_valid, photo_id = upload_photo(request.FILES)
            if not is_save_valid:
                return HttpResponseBadRequest("Invalid photo upload")

            user = User.objects.create_user(
                username=form_subscribe.cleaned_data['email'],
                email=form_subscribe.cleaned_data['email'],
                password=get_random_string(),
                first_name=form_subscribe.cleaned_data['first_name'],
                last_name=form_subscribe.cleaned_data['last_name']
            )
            user.save()

            doctor = Doctor(
                user=user,
                photo_id=photo_id,
                doctor_id=form_subscribe.cleaned_data['doctor_id'],
                speciality=form_subscribe.cleaned_data['speciality'],
                formation=form_subscribe.cleaned_data['formation']
            )
            doctor.save()

            location_1 = form_location_1.save()
            work_place_1 = form_work_place_1.save(commit=False)
            work_place_1.doctor = doctor
            work_place_1.location = location_1
            work_place_1.save()

            if nb_workplaces >= 2:
                location_2 = form_location_2.save()
                work_place_2 = form_work_place_2.save(commit=False)
                work_place_2.doctor = doctor
                work_place_2.location = location_2
                work_place_2.save()

            return render(request, "doctor/doctor_thanks_subscribe_view.html", {'doctor': doctor.get_info()})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()
