# Generated by Django 5.0.2 on 2024-02-12 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_hospital_alter_admin_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('specialization_id', models.AutoField(primary_key=True, serialize=False)),
                ('specialization_name', models.CharField(blank=True, max_length=200, null=True)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.hospital')),
            ],
        ),
    ]
