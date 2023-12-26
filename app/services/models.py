from random import choices
from django.db import models
from account.models import User
from commons.utils import TimeStampedModel
from app.settings import BASE_DIR
STATUS = (
    ('verified', 'verified'),
    ('unknown', 'unknown')
)

from services.code.prediction import license_plate_text_detection


class AppointmentSlot(TimeStampedModel):
    position = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(blank=False)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    slot_details = models.TextField(max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(default=None, null=True)
    fees = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return "User: " + str(self.created_by) + " | Date: " + str(self.date)+ " | Start_time: " + str(self.start_time)+ " | End_time: " + str(self.end_time)

from commons.utils import Util
class Appointment(TimeStampedModel):
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE,null=True,blank=True)
    is_accepted = models.BooleanField(default=None, null=True)
    is_paid = models.BooleanField(default=False)
    vehicle_image = models.ImageField(null=True, blank=True)
    license_plate = models.ImageField(null=True, blank=True)
    license_plate_text = models.CharField(max_length=50, null=True, blank=True)
    amount_paid = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        if self.is_accepted:
            accepted = 'Accepted'
        else:
            accepted = 'Rejected'
        return str(self.created_by) + " | " + str(self.slot) + " | " + str(accepted)


from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=Appointment)
def update_licenseplatetext(sender, instance, **kwargs):
    booked=False
    try:
        if instance.is_accepted == True and instance.is_paid == False:
            notifications_obj = Notification(
                created_by=instance.created_by, is_accepted=True,appointment=instance, text=f'{instance.created_by.name if instance.created_by.name else instance.created_by.email}, you have accepted "{instance.slot}" appointment slot. Please continue with payment!')
        elif instance.is_accepted == False and instance.is_paid == False:
            notifications_obj = Notification(
                created_by=instance.created_by, is_accepted=False,appointment=instance, text=f'{instance.created_by.name if instance.created_by.name else instance.created_by.email},you have rejected "{instance.slot}" appointment slot.')
        elif instance.is_accepted == True and instance.is_paid == True and instance.amount_paid>=instance.slot.fees:
            booked=True 
            notifications_obj = Notification(
                created_by=instance.created_by, is_accepted=True, appointment=instance, text='Payment successful for this appointment.')
        else:
            notifications_obj = Notification(
                created_by=instance.created_by, is_accepted=True, appointment=instance, text='Please complete appointment flow correctly!')

        notifications_obj.save()
        print("Notification saved")

        if instance.vehicle_image and instance.license_plate_text!=None:
            Util.send_email(instance.created_by.email, 'Admin Survelliance', notifications_obj.text,instance,BASE_DIR+instance.vehicle_image.url)          
            print("mail sent")
        
        if booked:
            print("Appointment booked successfully ")
            instance.slot.is_available=False 
            
    except Exception as e:
        print(e,"here there notifications")

    if instance.license_plate_text == None and instance.vehicle_image:
        img_url=instance.vehicle_image.url
        text=str(img_url)[1:]
        text=f"{BASE_DIR}/{text}"
        texts=list()
        for template in license_plate_text_detection(text):
            texts.append(template['prediction'][0]['ocr_text'])
        instance.license_plate_text=texts[0]
        print(f'Found texts in this image are : {texts}')
        try:
            user=User.objects.filter(license_plate_text=texts[0])[0]
            instance.created_by=user
        except Exception as e:
            print(e,"here there")
        instance.save()

class Notification(TimeStampedModel):
    text = models.TextField(max_length=500)
    datetime = models.DateTimeField(blank=True, auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,null=True, blank=True)
    is_accepted = models.BooleanField(default=None)

    def __str__(self):
        return "Notification: " + str(self.text)


class UserRecord(TimeStampedModel):
    vehicle_image = models.ImageField(blank=True, null=True, upload_to='user_vehicle_images/%Y%m%d')
    license_plate_image=models.ImageField(blank=True, null=True, upload_to='license_plate_images/%Y%m%d')
    licenseplatetext = models.CharField(max_length=100, blank=True, null=True)
    date=models.DateField(null=True, blank=True)
    entry_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=512, blank=True, null=True,choices=STATUS)
    parking_slot=models.ForeignKey('AppointmentSlot', on_delete=models.CASCADE,null=True,blank=True)
    parking_slot_details=models.CharField(max_length=1024, blank=True, null=True),
    amount_paid=models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.created_by) 

            

@receiver(post_save, sender=UserRecord)
def update_licenseplatetext(sender, instance, **kwargs):
    if instance.vehicle_image and instance.licenseplatetext == None:
        img_url=instance.vehicle_image.url
        text=str(img_url)[1:]
        text=f"{BASE_DIR}/{text}"
        texts=list()
        response=license_plate_text_detection(text)
        
        
        try:
            for template in response:
                texts.append(template['prediction'][0]['ocr_text'])
            
            instance.licenseplatetext=texts[0]
            print(f'Found texts in this image are : {texts}')   

            user=User.objects.filter(license_plate_text=texts[0])
            
            img_path=BASE_DIR+img_url
            if len(user)==0:
                Notification(
                    created_by=User.objects.get(id=1),
                    text='Unregistered user entered in survelliance  camera !'
                )
                Util.send_email('slyntherianknight@gmail.com',
                 'Admin Survelliance',
                 "Unregistered user entered in survelliance  camera !", instance,img_path)
            else:
                instance.created_by=user[0]
        except Exception as e:
            print(e,"license_plate ")
        

        # if appointment slot is available, create appointment
        try:
            if instance.created_by!=None and AppointmentSlot.objects.filter(is_available=True)[0] != None:
                print("entered if")
                slot_booked=False
                for slot in AppointmentSlot.objects.filter(is_available=True):  
                    print("enetered for loop")
                    try:
                        # create appointment for current user vehicle
                        print(1)
                        Appointment.objects.create(
                            slot=slot,
                            vehicle_image=instance.vehicle_image,
                            created_by=instance.created_by
                        )
                        # set current userrecord parking slot as this available slot
                        print(2)
                        instance.parking_slot=slot
                        
                        # make this slot unavailabe for others
                        print(3)
                        # slot.start_time ,slot.end_time
                        slot.is_available=False
                        
                        # slot booked
                        slot_booked=True
                        break 

                    except Exception as e:
                        print("Unable to create/book appointment/appointment_slot !",e)
                    
                    if slot_booked:
                        break 

        except Exception as e:
            print(e,"slot not created")
            
        instance.save()



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

