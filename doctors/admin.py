from django.contrib import admin
from doctors.models import ALLDOCTORS,Treatment,Appointment
# Register your models here.
admin.site.register(ALLDOCTORS)
admin.site.register(Treatment)
admin.site.register(Appointment)