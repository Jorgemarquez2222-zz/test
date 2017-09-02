from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from app_public.views import *

# Pages
from app_public.views.pages.doctor.doctor_group_view import ViewDoctorGroupView

my_urlpatterns = [
    # Home page
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),

    # Users
    #url(r'^login/$', ViewLogin.as_view(), name="login"),
    url(r'^subscribe/$', ViewSubscribeDoctor.as_view(), name="subscribe_doctor"),
    url(r'^thanks/$', ViewSubscribeThanksDoctor.as_view(), name="subscribe_thanks_doctor"),
    #url(r'^subscribe/$', ViewSubscribePatient.as_view(), name="subscribe_patient"),
    #url(r'^profile/d$', ViewProfileDoctor.as_view(), name="profile_doctor"),
    #url(r'^profile/$', ViewProfilePatient.as_view(), name="profile_patient"),

    # Doctor
    #url(r'^agenda/$', ViewAgenda.as_view(), name="agenda_view"),
    #url(r'^workplace/$', ViewWorkPlace.as_view(), name="work_place_view"),
    url(r'^doctorview/$', ViewDoctorView.as_view(), name="doctorview"),
    url(r'^profileview/$', TemplateView.as_view(template_name="doctor_profile_example.html"), name="doctor_profile_example_view"),
    url(r'^advantages/$', TemplateView.as_view(template_name="advantages.html"), name="advantages_view"),
    #url(r'^doctorgroupview/$', ViewDoctorGroupView.as_view(), name="doctorgroupview"),
    #url(r'^patientlist/$', ViewPatientList.as_view(), name="patientlist"),
    #url(r'^patientview/$', ViewPatientView.as_view(), name="patientview"),
    #url(r'^search/$', ViewSearch.as_view(), name="search"),

    #url(r'^test/$', ViewTest.as_view(), name="test"),
]

# Api (via /api/...)
my_urlpatterns_api = [
    # Users
    #url(r'^login/$', apiLogin, name="api_login"),
    #url(r'^logout/$', apiLogout, name="api_logout"),
    #url(r'^subscribe/d/$', apiSubscribeDoctor, name="api_subscribe_doctor"),
    #url(r'^subscribe/$', apiSubscribePatient, name="api_subscribe_patient"),
    #url(r'^profile/d/$', ApiProfileDoctor.as_view(), name="api_profile_doctor"),
    #url(r'^profile/$', ApiProfilePatient.as_view(), name="api_profile_patient"),

    # Doctor
    #url(r'^doctor/workplace/$', apiWorkPlace, name="api_workplace"),
    #url(r'^doctor/workschedule/$', ApiWorkschedule.as_view(), name="api_doctor_workschedule"),
    #url(r'^doctor/workschedule/remove/$', ApiWorkscheduleRemove.as_view(), name="api_workschedule_remove"),
    #url(r'^doctor/info/$', ApiDoctorInfo.as_view(), name="api_doctor_info"),
    #url(r'^doctor/getavailability/$', ApiGetAvailability.as_view(), name="api_get_availability"),
    #url(r'^appointmenttype/$', ApiAppointmentType.as_view(), name="api_appointment_type"),
    #url(r'^appointmenttype/get/$', apiAppointmentTypeGet, name="api_appointment_type_get"),
    #url(r'^appointmenttype/add/$', apiAppointmentTypeAdd, name="api_appointment_type_add"),
    #url(r'^appointmenttype/remove/$', apiAppointmentTypeRemove, name="api_appointment_type_remove"),
    url(r'^search/$', ApiSearch.as_view(), name="api_search"),
    #url(r'^searchpatient/$', apiSearchPatient, name="api_search_patient"),

    # Appointments
    #url(r'^appointments/make/$', apiAppointmentsMakePatient, name="api_appointments_make_patient"),
    #url(r'^appointments/make/d/$', apiAppointmentsMakeDoctor, name="api_appointments_make_doctor"),
    #url(r'^appointments/get/$', apiAppointmentsGet, name="api_appointments_get"),
    #url(r'^appointments/cancel/$', apiAppointmentsCancel, name="api_appointments_cancel"),
]

urlpatterns = [
    url(r'^', include(my_urlpatterns)),
    url(r'^api/', include(my_urlpatterns_api)),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/media/logo/logo_small.png', permanent=True))
]