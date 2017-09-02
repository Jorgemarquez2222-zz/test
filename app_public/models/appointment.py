from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from app_public.models.doctor import Doctor
from app_public.models.my_user import MyUser
from app_public.models.appointment_type import AppointmentType
from app_public.models.work_place import WorkPlace

from app_public.app.tools import filter_dict_fields


"""
"""


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    work_place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    patient = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointment_list")
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    start = models.DateTimeField(default=timezone.now, db_index=True)
    end = models.DateTimeField(default=timezone.now, db_index=True)
    name = models.CharField(max_length=100, blank=True)
    comment = models.TextField(max_length=5000, blank=True)
    APPOINTMENT_STATES = (
        ('n', _('Not Present')),
        ('w', _('Waiting')),
        ('c', _('Consulting')),
        ('f', _('Finished')),
        ('a', _('Cancelled')),
        ('e', _('Excused')),
    )
    state = models.CharField(max_length=1, choices=APPOINTMENT_STATES, default="n")

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'doctor': self.doctor.get_info(['id', 'first_name', 'last_name']),
                'patient': self.patient.get_info(['id', 'first_name', 'last_name']),
                'appointment_type': self.appointment_type.get_info(['id', 'name']),
                'start': self.start,
                'end': self.end,
                'name': self.name,
                'comment': self.comment,
                'state': self.state}
        if field_list is None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return 'Appointment at {}'.format(str(self.start))
