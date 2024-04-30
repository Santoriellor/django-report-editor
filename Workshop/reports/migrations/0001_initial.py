# Generated by Django 5.0.2 on 2024-03-17 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default='', max_length=50)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('phone_number1', models.CharField(default='', max_length=20)),
                ('phone_number2', models.CharField(blank=True, default='', max_length=20)),
                ('address', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=100)),
                ('client_info', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FuelFilter',
            fields=[
                ('ref_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('quantity', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Impeller',
            fields=[
                ('ref_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('quantity', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ref', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('stock_quantity', models.SmallIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OilFilter',
            fields=[
                ('ref_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('quantity', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='SparkPlug',
            fields=[
                ('ref_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('quantity', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='MotorModel',
            fields=[
                ('motor_model_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=50)),
                ('oil_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fuel_filter', models.ForeignKey(default='no Fuel Filter associated', on_delete=django.db.models.deletion.SET_DEFAULT, to='reports.fuelfilter')),
                ('impeller', models.ForeignKey(default='no Impeller associated', on_delete=django.db.models.deletion.SET_DEFAULT, to='reports.impeller')),
                ('oil_filter', models.ForeignKey(default='no Oil Filter associated', on_delete=django.db.models.deletion.SET_DEFAULT, to='reports.oilfilter')),
                ('spark_plug', models.ForeignKey(default='no Spark Plug associated', on_delete=django.db.models.deletion.SET_DEFAULT, to='reports.sparkplug')),
            ],
        ),
        migrations.CreateModel(
            name='MotorOwner',
            fields=[
                ('serial_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.client')),
                ('motor_model_number', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.motormodel')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_report', models.DateField(null=True)),
                ('info', models.CharField(blank=True, default='', max_length=50)),
                ('extras', models.TextField(blank=True, null=True)),
                ('exported', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reports.client')),
                ('motor_serial_number', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.motorowner')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reports.report')),
            ],
        ),
        migrations.CreateModel(
            name='ReportItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_quantity', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='reports.item')),
                ('report', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='reports.report')),
            ],
        ),
    ]
