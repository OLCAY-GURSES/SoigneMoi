from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    is_admin = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    login_status = models.BooleanField(default=False)

    def __str__(self):

        return self.email


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user.email)


class Hospital(models.Model):

    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='hospitals/', default='hospitals/default.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=10,null=True, blank=True)

    # String representation of object
    def __str__(self):
        return str(self.name)


class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    specialization_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        val1 = str(self.specialization_name)
        val2 = str(self.hospital)
        val3 = val1 + ' - ' + val2
        return str(val3)


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=10,null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Doctor(models.Model):

    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    reg_number = models.CharField(max_length=6, null=True, blank=True)
    hospital_name = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class DoctorTimeSlots(models.Model):
    # ForeignKey/ManyToMany
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doc_start_date = models.DateField(null=True, blank=True)
    doc_end_date= models.DateField(null=True, blank=True)

    def __str__(self):
        # doctor.get_full_name()
        return f"{self.doctor.first_name}.  Consulting Date: from {self.doc_start_date} to {self.doc_end_date}"

    class Meta:
        verbose_name_plural = "DoctorTimeSlots"


class Appointment(models.Model):

    appointment_id = models.AutoField(primary_key=True)
    doctor_time_slots = models.ForeignKey(DoctorTimeSlots, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    motif = models.TextField(null=False, blank=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, blank=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False, blank=False)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    choise_speciality=models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True, blank=True)

    #def __str__(self):
        #return f"{self.patient.first_name} booked an appointment from {self.doctor_time_slots.doc_start_date} to {self.doctor_time_slots.doc_end_date}"

    def __str__(self):
        return str(self.patient.last_name)

    class Meta:
        verbose_name_plural = "Appointment"


class Prescription(models.Model):
    # medicine name, quantity, days, time, description, test, test_descrip
    prescription_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateField(null=True, blank=True)
    extra_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.patient)


class Prescription_medicine(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='prescription_medicines', on_delete=models.CASCADE,
                                     null=True, blank=True)
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    dosage = models.CharField(max_length=200, null=True, blank=True)  # Added dosage field
    start_day = models.DateField(null=True, blank=True)
    end_day = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length=200, null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.medicine_id)


class Prescription_test(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='prescription_test', on_delete=models.CASCADE,
                                     null=True, blank=True)
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_description = models.TextField(null=True, blank=True)  # Added test_description field
    test_info_id = models.CharField(max_length=200, null=True, blank=True)
    test_results = models.TextField(null=True, blank=True)

def __str__(self):
        return str(self.test_id)


class Test_Information(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_description = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.test_name)

class Secretary(models.Model):

    secretary_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='secretary')
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    reg_number = models.CharField(max_length=6, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    hospital_name = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.user.email)
