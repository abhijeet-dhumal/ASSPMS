from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from account.models import User

class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password1', 'password2']

from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
    class Meta:
        model = User
        fields = "__all__"
        

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = '__all__'
#         widgets = {
#             'Starttime_of_appointment': forms.TextInput(
#                 attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
#         }

