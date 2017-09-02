from django.db import models

from app_public.models.doctor import Doctor

from app_public.app.tools import filter_dict_fields

"""
	Represents a medical speciality
		A dorcor can have multiple specialities
"""


class Speciality(models.Model):
    speciality = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="specialities")
    doctors = models.ManyToManyField(Doctor, blank=True, related_name="specialities")
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=3000, blank=True)
    validated = models.BooleanField(default=False, db_index=True)

    def get_info(self, field_list=None):
        info = {'id': self.id, 'name': self.name, 'type': self.__class__.__name__}
        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return str(self.name) + (" (V)" if self.validated else "")
