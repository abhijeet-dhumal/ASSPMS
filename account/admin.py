from django.contrib import admin
from django import forms

from account.models import RequestUpdateProfile, User, UserQuery, User_Query_Status


class UserQueryForm(forms.ModelForm):
    status = forms.ChoiceField(choices=User_Query_Status)

    class Meta:
        model = UserQuery
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name', 'dob', 'preferred_name',
         'user_type', 'pronoun', 'location', 'description', 'profile_image', 'vehicle_image','license_plate_text')}),
        (('Professional User Fields'), {'fields': (
            'company', 'experience', 'starting_charge_price', 'mode_of_service')}),
        (('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'dob',
                    'preferred_name', 'pronoun', 'is_staff')
    search_fields = ('email', 'name', 'preferred_name', 'pronoun')
    ordering = ('email',)


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pronoun', 'email', 'phone', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'pronoun', 'email')
    form = UserQueryForm


admin.site.register(RequestUpdateProfile)

admin.site.register(User, UserAdmin)
admin.site.register(UserQuery, UserQueryAdmin)
