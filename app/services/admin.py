from django.contrib import admin
from services.models import *
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AppointmentSlot)
admin.site.register(Notification)
admin.site.register(UserRecord)