import logging
from django.db.models import Q
from app_public.models import Doctor, Patient, Speciality, DoctorGroup, WorkPlace, Location
from app_public.app.Configuration import FILE_HANDLER

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


def search_doctor_by_name(search_text):
    q_req = Q()
    for word in search_text.split(' '):
        q_req = q_req | Q(user__first_name__icontains=word)
        q_req = q_req | Q(user__last_name__icontains=word)

    users = Doctor.objects.filter(q_req).order_by('user__last_name', 'user__first_name')

    return users


def search_patient_by_name(search_text):
    q_req = Q()
    for word in search_text.split(' '):
        q_req = q_req | Q(user__first_name__icontains=word)
        q_req = q_req | Q(user__last_name__icontains=word)

    users = Patient.objects.filter(q_req).order_by('user__last_name', 'user__first_name')

    return users


def search_doctor_by_distance(longitude, latitude, speciality):
    lon = str(longitude)
    lat = str(latitude)
    formula = "address__longitude - {} + address__latitude - {}".format(lon, lat)
    query = speciality.doctors.extra(select={'distance': formula}).order_by('-distance')
    return None


def search_speciality_by_name(search_text):
    q_req = Q()
    for word in search_text.split(' '):
        q_req = q_req | Q(name__icontains=word)

    query = Speciality.objects.filter(Q(validated=True) & q_req)

    return query


def search_group_by_name(search_text):
    q_req = Q()
    for word in search_text.split(' '):
        q_req = q_req | Q(name__icontains=word)

    query = DoctorGroup.objects.filter(q_req)

    return query
