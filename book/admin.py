from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from book.models import User, Hospital, Specialization, Admin, Patient, Doctor,DoctorTimeSlots

admin.site.register(Hospital)
admin.site.register(Specialization)
admin.site.register(Admin)
admin.site.register(Patient)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','specialization']

admin.site.register(Doctor, DoctorAdmin)


class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['Doctor_first_name','Doctor_last_name', 'doc_start_date', 'doc_end_date']

    # Method to display the doctors Name in the Django admin dashboard.it overrides the __str__ method in the models.py
    def Doctor_first_name(self, doctorTimeSlots):
        return doctorTimeSlots.doctor.first_name

    def Doctor_last_name(self, doctorTimeSlots):
        return doctorTimeSlots.doctor.last_name

admin.site.register(DoctorTimeSlots, DoctorTimeSlotsAdmin)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_admin','is_patient','is_doctor')}),

        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'is_admin','is_patient','is_doctor')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)