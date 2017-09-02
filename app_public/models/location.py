from django.db import models

from app_public.app.tools import filter_dict_fields


"""
	Represents a medical speciality
		A dorcor can have multiple specialities
    Backward relations
        work_places
"""


class Location(models.Model):
    address = models.CharField(max_length=200, blank=True, default="")
    longitude = models.DecimalField(default=0, max_digits=12,
                                    decimal_places=8, db_index=True,
                                    null=True, blank=True)
    latitude = models.DecimalField(default=0, max_digits=12,
                                   decimal_places=8, db_index=True,
                                   null=True, blank=True)

    def get_info(self, field_list=None):
        info = {'id': self.id,
                'address': self.address,
                'longitude': self.longitude,
                'latitude': self.latitude}
        if field_list == None:
            return info
        return filter_dict_fields(info, field_list)

    def __str__(self):
        return "{} : {}".format(str(self.id), str(self.address))