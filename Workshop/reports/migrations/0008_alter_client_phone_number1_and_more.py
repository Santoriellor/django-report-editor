# Generated by Django 5.0.2 on 2024-03-20 08:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_alter_reportitem_report_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number1',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
