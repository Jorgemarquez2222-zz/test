from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from app_public.models.location import Location

from app_public.app.tools import filter_dict_fields
from app_public.models.fields import MyPhoneField


"""
    Base class for Doctor and Patient
"""


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="my_user")
    address = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name="my_users")
    phone = MyPhoneField()
    birth_date = models.DateField(null=True)
    SEXES = (
        ('m', _('Male')),
        ('f', _('Female')),
    )
    sexe = models.CharField(max_length=1, choices=SEXES, default="m")


    """
        In all classes, thos function returns all data 'serialized'
        restricted to fields in 'field_list' if present
    """


    def get_info(self, field_list=None):
        info = {'id': self.get_id(),
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'birth_date': self.birth_date,
                'sexe': self.sexe,
                'phone': self.phone,
                'address': str(self.address.address) if not self.address is None else None}
        if field_list == None:
            return info
        return filter_dict_fields(info, field_list)

    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} : {} {} ({})".format(self.get_id(), self.user.first_name, self.user.last_name, self.user.username)
