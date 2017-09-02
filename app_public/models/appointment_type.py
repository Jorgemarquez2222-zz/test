from django.db import models
from datetime import timedelta

from app_public.models.fields import MyPriceField, MyColorField
from app_public.models.doctor import Doctor
from app_public.models.work_place import WorkPlace

from app_public.app.tools import filter_dict_fields


"""
    Represents the different types of appointments a doctor can have
        validated : When an appointment type is validated, it is available for everyone
    Backward relations
        appointments
        work_schedules
"""


class AppointmentType(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointment_types")
    work_place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointment_types")
    validated = models.BooleanField(default=False, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    duration = models.DurationField(default=timedelta(minutes=30))
    price = MyPriceField()
    color = MyColorField()
    reservable = models.BooleanField(default=True, db_index=True)

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'validated': self.validated,
                'name': self.name,
                'duration': str(self.duration),
                'price': self.price,
                'color': self.color}
        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return "{} : {}{}".format(str(self.id), str(self.name), " (V)" if self.validated else "")
