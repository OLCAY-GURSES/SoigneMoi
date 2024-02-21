from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, User, Admin, Doctor

import random
import string


def generate_random_string():
    N = 6
    string_var = ""
    string_var = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=N))
    string_var = "#PT" + string_var
    return string_var


@receiver(post_save, sender=User)
def createPatient(sender, instance, created, **kwargs):
    if created:
        if instance.is_patient:
            user = instance
            Patient.objects.create(
                user=user, serial_number=generate_random_string())
        elif instance.is_doctor:
            user = instance
            Doctor.objects.create(
                user=user)



@receiver(post_save, sender=Patient)
def updateUser(sender, instance, created, **kwargs):
    # user.profile or below (1-1 relationship goes both ways)
    patient = instance
    user = patient.user

    if created == False:
        user.last_name = patient.last_name
        user.first_name = patient.first_name
        user.email = user.email
        user.save()
