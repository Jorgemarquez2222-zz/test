from django.core.exceptions import ObjectDoesNotExist

from app_public.models import Doctor, Patient

"""
	Returns the doctor corresponding to the specified id or None if not found
"""


def get_doctor_by_id(user_id):
    try:
        return Doctor.objects.get(user__id=user_id)
    except ObjectDoesNotExist:
        return None

"""
    Returns the Patient corresponding to the specified id or None if not found
"""


def get_patient_by_id(user_id):
    try:
        return Patient.objects.get(user__id=user_id)
    except ObjectDoesNotExist:
        return None

"""
    Returns the user corresponding to the specified id or None if not found
"""


def get_my_user_by_id(user_id):
    my_user = get_doctor_by_id(user_id)
    if my_user is None:
        my_user = get_patient_by_id(user_id)
    return my_user

"""
	Returns the doctor corresponding to the specified user or None if not found
"""


def get_doctor(user):
    try:
        return Doctor.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


"""
	Returns the patient corresponding to the specified user or None if not found
"""


def get_patient(user):
    try:
        return Patient.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


"""
	Tests if user is a doctor
"""


def is_doctor(user):
    return Doctor.objects.filter(user=user).exists()


"""
	Tests if user is a patient
"""


def is_patient(user):
    return Patient.objects.filter(user=user).exists()


"""
	Returns the corresponding doctor or patient if present, or None if not found
"""


def get_my_user(user):
    my_user = get_doctor(user)
    if my_user is None:
        my_user = get_patient(user)
    return my_user
