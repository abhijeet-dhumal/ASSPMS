from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserRecordForm(forms.ModelForm):
    
    class Meta:
        model = UserRecord
        fields = '__all__'

import datetime
class AppointmentSlotForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = AppointmentSlot
        fields = '__all__'
        widgets = {
            'start_time': forms.TextInput(
                attrs={'placeholder': 'HH:MM AM/PM'}),
            'end_time': forms.TextInput(
                attrs={'placeholder': 'HH:MM AM/PM'}),
        }

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'start_time': forms.TextInput(
                attrs={'placeholder': 'HH:MM AM/PM'}),
            'end_time': forms.TextInput(
                attrs={'placeholder': 'HH:MM AM/PM'}),
        }
