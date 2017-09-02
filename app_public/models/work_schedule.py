from django.db import models
from datetime import timedelta, datetime

from app_public.models.doctor import Doctor
from app_public.models.appointment_type import AppointmentType
from app_public.models.work_place import WorkPlace
from app_public.models.fields import MyColorField

from app_public.app.tools import filter_dict_fields


"""
    Represents a time slot group during which the Doctor is available and can receive appointments
    This contains simple time slots (One or several if recurrent)
        appointment_types : appointment types available on that slot
    Backward relation fields
        available_slots
"""


class WorkSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="work_schedules")
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, null=True, blank=True, related_name="work_schedules")
    appointment_types = models.ManyToManyField(AppointmentType, related_name="work_schedules")
    name = models.CharField(max_length=100, blank=True)
    granularity = models.DurationField(default=timedelta(minutes=30))
    reservable = models.BooleanField(default=True, db_index=True)
    color = MyColorField()
    recurrent = models.BooleanField(default=False, db_index=True)
    repeat_day_1 = models.BooleanField(default=False, db_index=True) # Monday
    repeat_day_2 = models.BooleanField(default=False, db_index=True)
    repeat_day_3 = models.BooleanField(default=False, db_index=True)
    repeat_day_4 = models.BooleanField(default=False, db_index=True)
    repeat_day_5 = models.BooleanField(default=False, db_index=True)
    repeat_day_6 = models.BooleanField(default=False, db_index=True)
    repeat_day_7 = models.BooleanField(default=False, db_index=True)
    repeat_until = models.DateTimeField(default=datetime.utcnow, null=True, db_index=True) # If Null, repeat always
    start = models.DateTimeField(default=datetime.utcnow)
    end = models.DateTimeField(default=datetime.utcnow)

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'name': self.name,
                'granularity': str(self.granularity),
                'color': self.color,
                'recurrent': self.recurrent,
                'dow': [],
                'repeat_until': self.repeat_until,
                'start': self.start,
                'end': self.end}
        if self.repeat_day_1:
            info.dow.push(1)
        if self.repeat_day_2:
            info.dow.push(2)
        if self.repeat_day_3:
            info.dow.push(3)
        if self.repeat_day_4:
            info.dow.push(4)
        if self.repeat_day_5:
            info.dow.push(5)
        if self.repeat_day_6:
            info.dow.push(6)
        if self.repeat_day_7:
            info.dow.push(7)
        if field_list == None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return '{} : {}'.format(str(self.doctor), str(self.name))