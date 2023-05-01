from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserRecordForm(forms.ModelForm):
    
    class Meta:
        model = UserRecord
        fields = '__all__'

import pytz, datetime
utc = pytz.utc
class AppointmentSlotForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        
