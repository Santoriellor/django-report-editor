# Generated by Django 5.0.2 on 2024-03-17 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_item_label_alter_reportitem_report_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='info',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]