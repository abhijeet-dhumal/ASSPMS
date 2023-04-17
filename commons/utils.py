from django.db import models
from account.models import User
from app.settings import EMAIL_HOST_USER
from .PostgresDataTime import DateTimeWithoutTZField as DateTimeField

class TimeStampedModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True, null=True)
    class Meta:
        abstract = True


from rest_framework import serializers 

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage 
import os
import threading
from django.conf import settings
from app.settings import BASE_DIR

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


    @staticmethod
    def otp_keygen(email):
        return f"{email}-{settings.SECRET_KEY}"

    @staticmethod
    def send_email(email, subject, message,instance=None,img_path=None):
        if(instance.created_by==None):
            try:
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.license_plate_text}</p>
                        <p>Entry time : {instance.created_at}</p>
                    </body>
                </html>
                '''
            except : 
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.licenseplatetext}</p>
                        <p>Entry time : {instance.created_at}</p>
                    </body>
                </html>
                '''
        else:
            try:
                body_html = f'''
                <html>
                    <body>
                        <h2>Admin Survelliance</h2>
                        <p>License plate text : {instance.license_plate_text}</p>
                        <p>Entry time : {instance.created_at}</p>
                        <p>Slot : {instance.slot}</p>
                        <p> Slot position : {instance.slot.position}</p>
                        <p> Slot details : {instance.slot.slot_details}</p>
                        <p> Is verified : {instance.slot.is_verified}</p>
                        <p> Fees paid : {instance.slot.fees}</p>
                    </body>
                </html>
                '''
            except:
                body_html = f'''
            <html>
                <body>
                    <h2>Admin Survelliance</h2>
                    <p>License plate text : {instance.licenseplatetext}</p>
                    <p>Entry time : {instance.created_at}</p>
                    <p>Slot : {instance.slot}</p>
                </body>
            </html>
            '''

        msg = EmailMultiAlternatives(
            to=[email], 
            body=message, 
            subject=subject, 
            from_email=EMAIL_HOST_USER
        )

        msg.mixed_subtype = 'related'
        msg.attach_alternative(body_html, "text/html")
        if img_path :
            image_name=img_path.split("/")[-1]
            
            with open(img_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<{name}>'.format(name=image_name))
                img.add_header('Content-Disposition', 'inline', filename=image_name)
            msg.attach(img)

        EmailThread(msg).start()
    
    @staticmethod
    def base64_to_file(data,url_address=None):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        import time
        
        if data != None:
            
            named_tuple = time.localtime() # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            try:
                format, uri = data.split(';base64,')
                file = ContentFile(base64.urlsafe_b64decode(uri), name=f"VehicleImage-{time_string}.{format.split('/')[-1]}")
            except Exception as e:
                file_name = str(uuid.uuid4())[:12] 
                decoded_file=base64.urlsafe_b64decode(data)
                extension = url_address.split("/")[-1].split(".")[-1]
                complete_file_name = f"{file_name}.{extension}"

                file = ContentFile(decoded_file, name=complete_file_name)
            return file
        else:
            return None

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
