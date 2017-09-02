from django.contrib import admin
from app_public.models import *

admin.site.register(Appointment)
admin.site.register(AppointmentType)
admin.site.register(AvailableSlot)
admin.site.register(Doctor)
admin.site.register(DoctorGroup)
admin.site.register(Location)
admin.site.register(MyUser)
admin.site.register(Patient)
admin.site.register(Speciality)
admin.site.register(WorkPlace)
admin.site.register(WorkSchedule)