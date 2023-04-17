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
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),)
    start_time = forms.TimeField(widget=forms.widgets.TimeInput(format='%I:%M %P',attrs={'placeholder': 'HH:MM am/pm'}))
    end_time = forms.TimeField(widget=forms.widgets.TimeInput(format='%I:%M %P',attrs={'placeholder': 'HH:MM am/pm'}))

    class Meta:
        model = AppointmentSlot
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),)
    start_time = forms.TimeField(widget=forms.widgets.TimeInput(format='%I:%M %P',attrs={'placeholder': 'HH:MM am/pm'}))
    end_time = forms.TimeField(widget=forms.widgets.TimeInput(format='%I:%M %P',attrs={'placeholder': 'HH:MM am/pm'}))

    class Meta:
        model = Appointment
        fields = '__all__'
        
