# Generated by Django 5.0.2 on 2024-03-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_report_date_report_alter_report_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='info',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
