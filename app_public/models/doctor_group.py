from django.db import models
from django.urls import reverse

from app_public.models.doctor import Doctor

from app_public.app.tools import filter_dict_fields


"""
	This represents a doctor group
	   Ex : Hospital, cabinet
"""


class DoctorGroup(models.Model):
    doctors = models.ManyToManyField(Doctor, blank=True, related_name="doctor_groups")
    name = models.CharField(max_length=100, blank=True, db_index=True)
    description = models.TextField(max_length=5000, blank=True)

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'name': self.name,
                'type': self.__class__.__name__,
                'url' : reverse('doctorgroupview') + "?id=" + str(self.id),
                'photo_url' : "/static/media/logo/logo.png"}

        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return str(self.name)