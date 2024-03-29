# Generated by Django 5.0.2 on 2024-02-22 17:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0011_test_information_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_secretary",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Secretary",
            fields=[
                ("secretary_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=200, null=True)),
                ("last_name", models.CharField(max_length=200, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("date_of_bird", models.DateField(blank=True, null=True)),
                ("reg_number", models.CharField(blank=True, max_length=6, null=True)),
                (
                    "hospital_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="book.hospital",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secretary",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
