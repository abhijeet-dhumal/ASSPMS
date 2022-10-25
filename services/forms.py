from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserRecordForm(forms.ModelForm):
    
    class Meta:
        model = UserRecord
        fields = '__all__'