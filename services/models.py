from random import choices
from django.db import models
from account.models import User,TimeStampedModel
STATUS = (
    ('verified', 'verified'),
    ('unknown', 'unknown')
)

from services.nanonets_ocr_sample_python.code.prediction import license_plate_text_detection

class UserRecord(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_image = models.ImageField(blank=True, null=True, upload_to='user_vehicle_images/%Y%m%d')
    license_plate_image=models.ImageField(blank=True, null=True, upload_to='license_plate_images/%Y%m%d')
    license_plate_text = models.CharField(max_length=100, blank=True, null=True)
    entry_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=512, blank=True, null=True,choices=STATUS)
    parking_slot_details=models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return str(self.user) 


class AppointmentSlot(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    slot_details = models.TextField(max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(default=None, null=True)

    def __str__(self):
        return "User: " + str(self.user) + " | Date: " + str(self.date)

class Appointment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=None, null=True)
    is_paid = models.BooleanField(default=False)
    vehicle_image = models.ImageField()
    license_plate = models.ImageField()
    license_plate_text = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True,blank=True)

    def __str__(self):
        if self.is_accepted:
            accepted = 'Accepted'
        else:
            accepted = 'Rejected'
        return str(self.user) + " | " + str(self.slot) + " | " + str(accepted)

    def save(self, *args, **kwargs):
        if self.is_accepted != None:
            if self.is_accepted == True and self.is_paid == False:
                notifications_obj = Notification(
                    user=self.user, is_accepted=True, appointment=self, text=f'{self.slot.professional_user.name} has accepted your appointment request.')
            elif self.is_accepted == False and self.is_paid == False:
                notifications_obj = Notification(
                    user=self.user, is_accepted=False, appointment=self, text=f'{self.slot.professional_user.name} has rejected your appointment request.')
            elif self.is_accepted == True and self.is_paid == True:
                notifications_obj = Notification(
                    user=self.user, is_accepted=True, appointment=self, text='Payment successful for this appointment.')

            notifications_obj.save()

        super().save(*args, **kwargs)

from account.utils import Util
class Notification(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    datetime = models.DateTimeField(blank=True, auto_now_add=True)
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,null=True, blank=True)
    is_accepted = models.BooleanField(default=None)

    def __str__(self):
        return "Notification: " + str(self.text)

    # def save(self, *args, **kwargs):
    #     if self.is_accepted != None:
    #         if self.is_accepted == True and self.is_paid == False:
    #             notifications_obj = Notification(
    #                 user=self.user, is_accepted=True, appointment=self, text=f'{self.slot.user.name} has accepted your appointment request.')
    #         elif self.is_accepted == False and self.is_paid == False:
    #             notifications_obj = Notification(
    #                 user=self.user, is_accepted=False, appointment=self, text=f'{self.user.name} has rejected your appointment request.')
    #         elif self.is_accepted == True and self.is_paid == True:
    #             notifications_obj = Notification(
    #                 user=self.user, is_accepted=True, appointment=self, text='Payment successful for this appointment.')
    #         data = {'email_body': (notifications_obj.text), 'to_email': 'slyntherianknight@gmail.com',
    #                 'email_subject': 'Admin Survelliance'}
    #         Util.send_email(data)            
    #         notifications_obj.save()

        # super().save(*args, **kwargs)