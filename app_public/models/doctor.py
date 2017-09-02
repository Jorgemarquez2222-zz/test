from django.db import models
from django.urls import reverse

from app_public.models.my_user import MyUser

from app_public.app.tools import filter_dict_fields
from app_public.app.Configuration import FILE_HANDLER
from app_public.models.fields import MyPhotoIdField


"""
    Doctor model
        appointment_types : The doctor can create appointment types
        doctor_groups : Will be managed later
    Backward relation fields
        appointments
        appointment_types
        doctor_groups
        specialities
        work_places
        work_schedules
"""


class Doctor(MyUser):
    photo_id = MyPhotoIdField()
    doctor_id = models.TextField(max_length=100, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    formation = models.TextField(max_length=3000, blank=True)
    languages = models.TextField(max_length=1000, blank=True)
    speciality = models.TextField(max_length=100, blank=True)
    practical_informations = models.TextField(max_length=3000, blank=True)
    displayable = models.BooleanField(default=False, db_index=True)

    def get_info(self, field_list=None):
        info = super(Doctor, self).get_info(field_list)
        info['type'] = self.__class__.__name__
        info['description'] = self.description
        info['speciality'] = ''
        info['doctor_id'] = self.doctor_id
        info['formation'] = self.formation
        info['languages'] = self.languages
        info['practical_informations'] = self.practical_informations
        for s in self.specialities.all():
            if info['speciality'] == '':
                info['speciality'] += str(s)
            else:
                info['speciality'] += ", " + str(s)
        info['photo_url'] = FILE_HANDLER.get_url(self.photo_id) if self.photo_id != "" else \
            ("/static/media/logo/logo.png" if self.sexe == 'm' else "/static/media/logo/logo.png")
        info['url'] = reverse('doctorview') + "?id=" + str(self.get_id())
        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)

    def get_appointment_type(self, app_type_id=None):
        if app_type_id is not None:
            app_type = self.appointment_types.filter(id=app_type_id)
            if app_type.exists():
                return app_type.get()
            raise Exception("No appointment type.")

        if self.appointment_types.exists():
            return self.appointment_types[0]
        if self.specialities.exists():
            return self.specialities[0].default_appointment_type
        raise Exception("No appointment type for doctor " + self.user.username)