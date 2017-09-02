from django.db import models

from app_public.models.doctor import Doctor
from app_public.models.location import Location
from app_public.models.fields import MyColorField

from app_public.app.tools import filter_dict_fields
from app_public.models.fields import MyPhoneField


"""
	Represents a medical speciality
		A dorcor can have multiple specialities
    Backward relation field
        appointments
        appointment_types
        work_schedules
"""


class WorkPlace(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="work_places")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="work_places")
    name = models.CharField(max_length=500, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    work_slots = models.TextField(max_length=3000, blank=True)
    payment_method = models.CharField(max_length=500, blank=True)
    ensurance = models.CharField(max_length=500, blank=True)
    phone = MyPhoneField()
    color = MyColorField()

    def get_info(self, field_list=None):
        info = {'id': self.id, 'name': self.name, 'description': self.description, 'phone': self.phone}
        if field_list == None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return "{} : {} : {}".format(str(self.id), str(self.doctor), str(self.name))