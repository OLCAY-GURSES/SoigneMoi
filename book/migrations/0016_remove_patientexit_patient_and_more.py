# Generated by Django 5.0.2 on 2024-02-22 19:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0015_secretary_appointment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patientexit",
            name="patient",
        ),
        migrations.RemoveField(
            model_name="patientexit",
            name="secretary",
        ),
        migrations.DeleteModel(
            name="PatientEntry",
        ),
        migrations.DeleteModel(
            name="PatientExit",
        ),
    ]