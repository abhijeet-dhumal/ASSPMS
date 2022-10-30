from django.contrib import admin
from django import forms

from account.models import RequestUpdateProfile, User, User_Query_Status
from services.models import UserQuery

class UserQueryForm(forms.ModelForm):
    status = forms.ChoiceField(choices=User_Query_Status)

    class Meta:
        model = UserQuery
        fields = '__all__'

from django.contrib.auth.admin import UserAdmin

class UserAdminCustom(UserAdmin):

    fieldsets = (
        (('Personal Info'), {'fields': ('email', 'name', 'profile_image','password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id','email', 'name', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)    


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pronoun', 'email', 'phone', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'pronoun', 'email')
    form = UserQueryForm


admin.site.register(RequestUpdateProfile)

admin.site.register(User, UserAdminCustom)
admin.site.register(UserQuery, UserQueryAdmin)
