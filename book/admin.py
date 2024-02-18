from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from book.models import User, Hospital, Specialization, Admin, Patient, Doctor, DoctorTimeSlots, Appointment, \
    Prescription, Prescription_medicine, Prescription_test
import random
import string

admin.site.register(Hospital)
admin.site.register(Specialization)
admin.site.register(Admin)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Prescription_medicine)
admin.site.register(Prescription_test)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'first_name', 'last_name', 'specialization', 'phone_number', 'date_of_bird','reg_number',  'hospital_name')
    # other model administratif

    def save_model(self, request, obj, form, change):
        if not obj.reg_number:
            # Generate a random registration number
            reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Check if the generated registration number is already assigned to another doctor
            while Doctor.objects.filter(reg_number=reg_number).exists():
                reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            obj.reg_number = reg_number
        super().save_model(request, obj, form, change)


admin.site.register(Doctor, DoctorAdmin)



class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['Doctor_first_name','Doctor_last_name', 'doc_start_date', 'doc_end_date']

    # Method to display the doctors Name in the Django admin dashboard.it overrides the __str__ method in the models.py
    def Doctor_first_name(self, doctorTimeSlots):
        return doctorTimeSlots.doctor.first_name

    def Doctor_last_name(self, doctorTimeSlots):
        return doctorTimeSlots.doctor.last_name

admin.site.register(DoctorTimeSlots, DoctorTimeSlotsAdmin)

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['appointment_id','patient_last_name','patient_first_name', 'appointment_date','start_date', 'end_date','doctors']

    def patient_last_name(self, appointment):
        return appointment.patient.last_name

    patient_last_name.short_description = 'Last Name Patient'

    def patient_first_name(self, appointment):
        return appointment.patient.first_name

    patient_first_name.short_description = 'First Name Patient'

    def doctors(self, appointment):
        return appointment.doctor.last_name,appointment.doctor.first_name,

    doctors.short_description = 'Doctor'

    def appointment_date(self, appointment):

        return appointment.start_date
    appointment_date.short_description = 'Appointment Date'


admin.site.register(Appointment, AppointmentsAdmin)

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