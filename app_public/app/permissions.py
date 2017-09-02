from app_public.app.model import is_doctor, is_patient

def test_is_doctor(user):
	return is_doctor(user)

def test_is_patient(user):
	return is_patient(user)

def test_is_patient_or_doctor(user):
	return test_is_patient(user) or test_is_doctor(user)

def test_is_doctor_subscribed(user):
	# TODO : Test if doctor has an active subscription
	return True