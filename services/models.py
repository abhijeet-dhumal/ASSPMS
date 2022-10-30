from random import choices
from django.db import models
from account.models import User
from commons.utils import TimeStampedModel

STATUS = (
    ('verified', 'verified'),
    ('unknown', 'unknown')
)

from services.code.prediction import license_plate_text_detection

class UserRecord(TimeStampedModel):
    vehicle_image = models.ImageField(blank=True, null=True, upload_to='user_vehicle_images/%Y%m%d')
    license_plate_image=models.ImageField(blank=True, null=True, upload_to='license_plate_images/%Y%m%d')
    licenseplatetext = models.CharField(max_length=100, blank=True, null=True)
    entry_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=512, blank=True, null=True,choices=STATUS)
    parking_slot_details=models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return str(self.created_by) 

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=UserRecord)
def update_licenseplatetext(sender, instance, **kwargs):
    if instance.licenseplatetext == None:
        img_url=instance.vehicle_image.url
        text=str(img_url)[1:]
        print(text)
        texts=list()
        for template in license_plate_text_detection(text):
            texts.append(template['prediction'][0]['ocr_text'])
        instance.licenseplatetext=texts[0]
        print(f'Found texts in this image are : {texts}')
        instance.save()


class AppointmentSlot(TimeStampedModel):
    position = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(blank=False)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    slot_details = models.TextField(max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(default=None, null=True)

    def __str__(self):
        return "User: " + str(self.created_by) + " | Date: " + str(self.date)

class Appointment(TimeStampedModel):
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=None, null=True)
    is_paid = models.BooleanField(default=False)
    vehicle_image = models.ImageField(null=True, blank=True)
    license_plate = models.ImageField(null=True, blank=True)
    license_plate_text = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True,blank=True)

    def __str__(self):
        if self.is_accepted:
            accepted = 'Accepted'
        else:
            accepted = 'Rejected'
        return str(self.created_by) + " | " + str(self.slot) + " | " + str(accepted)

    def save(self, *args, **kwargs):
        # if self.is_accepted != None:
        #     if self.is_accepted == True and self.is_paid == False:
        #         notifications_obj = Notification(
        #             user=self.user, is_accepted=True, appointment=self, text=f'{self.slot.professional_user.name} has accepted your appointment request.')
        #     elif self.is_accepted == False and self.is_paid == False:
        #         notifications_obj = Notification(
        #             user=self.user, is_accepted=False, appointment=self, text=f'{self.slot.professional_user.name} has rejected your appointment request.')
        #     elif self.is_accepted == True and self.is_paid == True:
        #         notifications_obj = Notification(
        #             user=self.user, is_accepted=True, appointment=self, text='Payment successful for this appointment.')

        #     notifications_obj.save()

        super().save(*args, **kwargs)

from commons.utils import Util
class Notification(TimeStampedModel):
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

class UserQuery(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    pronoun = models.CharField(max_length=1024, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=512, blank=True, null=True)
    query = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)