# Generated by Django 5.0.2 on 2024-03-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_reportitem_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportitem',
            name='report_quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
    ]
