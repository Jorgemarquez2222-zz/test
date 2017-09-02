from app_public.models.my_user import MyUser
from django.urls import reverse


"""
	Patient model
    Backward relation fields
    	appointment_list
"""


class Patient(MyUser):
    def get_info(self, field_list=None):
        info = super(Patient, self).get_info(field_list)
        info['url'] = reverse("patientview") + "?id=" + str(self.get_id())
        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)