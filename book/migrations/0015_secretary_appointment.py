# Generated by Django 5.0.2 on 2024-02-22 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0014_remove_secretary_patients_of_the_day"),
    ]

    operations = [
        migrations.AddField(
            model_name="secretary",
            name="appointment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="book.appointment",
            ),
        ),
    ]