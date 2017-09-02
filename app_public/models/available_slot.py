from django.db import models
from datetime import datetime
from app_public.app.tools import filter_dict_fields

from app_public.models.work_schedule import WorkSchedule


"""
    Represents a time slot during which the Doctor is free and can receive appointments
    Backward relation fields
"""


class AvailableSlot(models.Model):
    work_schedule = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, related_name="available_slots")
    start = models.DateTimeField(default=datetime.utcnow, db_index=True)
    end = models.DateTimeField(default=datetime.utcnow, db_index=True)

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'start': self.start,
                'end': self.end}
        if field_list == None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return 'Available slot from {} to {}'.format(str(self.start), str(self.end))