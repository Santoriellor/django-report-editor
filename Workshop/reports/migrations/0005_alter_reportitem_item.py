# Generated by Django 5.0.2 on 2024-03-19 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_reportitem_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportitem',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reports.item'),
        ),
    ]