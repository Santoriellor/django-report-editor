from django.core.validators import RegexValidator
from django.db import models

# By default, Django automatically adds an integer primary key field to each model, called id
# By default, integer fields in Django models are auto-incremented.
# If blank=True then the form field will be required=False, else required=True

default_char = ''


# Create your models here.
class Client(models.Model):
    last_name = models.CharField(max_length=50, default=default_char)
    first_name = models.CharField(max_length=50, default=default_char)
    phone_number1 = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$",
            message='Enter a valid phone number.'
        )
    ])
    phone_number2 = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Enter a valid phone number.'
        )],
        blank=True
    )
    address = models.CharField(max_length=100, default=default_char, blank=True)
    email = models.CharField(max_length=100, default=default_char, blank=True)
    client_info = models.CharField(max_length=255, default=default_char, blank=True)

    def __str__(self):
        return f"{self.last_name.capitalize()} {self.first_name.capitalize()}"


class SparkPlug(models.Model):
    ref_number = models.CharField(primary_key=True, max_length=50)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)


class OilFilter(models.Model):
    ref_number = models.CharField(primary_key=True, max_length=50)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)


class FuelFilter(models.Model):
    ref_number = models.CharField(primary_key=True, max_length=50)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)


class Impeller(models.Model):
    ref_number = models.CharField(primary_key=True, max_length=50)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)


class MotorModel(models.Model):
    motor_model_number = models.CharField(primary_key=True, max_length=50)
    brand = models.CharField(max_length=50)
    # The 'spark_plug' field will be created as 'spark_plug_id' in the database because of the foreignkey
    spark_plug = models.ForeignKey(
        SparkPlug,
        on_delete=models.SET_DEFAULT,
        default='no Spark Plug associated',
        to_field='ref_number'
    )
    # The 'oil_filter' field will be created as 'oil_filter_id' in the database because of the foreignkey
    oil_filter = models.ForeignKey(
        OilFilter,
        on_delete=models.SET_DEFAULT,
        default='no Oil Filter associated',
        to_field='ref_number'
    )
    oil_quantity = models.DecimalField(max_digits=5, decimal_places=2)
    # The 'fuel_filter' field will be created as 'fuel_filter_id' in the database because of the foreignkey
    fuel_filter = models.ForeignKey(
        FuelFilter,
        on_delete=models.SET_DEFAULT,
        default='no Fuel Filter associated',
        to_field='ref_number'
    )
    # The 'impeller' field will be created as 'impeller_id' in the database because of the foreignkey
    impeller = models.ForeignKey(
        Impeller,
        on_delete=models.SET_DEFAULT,
        default='no Impeller associated',
        to_field='ref_number'
    )
    price = models.DecimalField(max_digits=15, decimal_places=2)


class MotorOwner(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=50)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    motor_model_number = models.ForeignKey(
        MotorModel,
        on_delete=models.SET_NULL,
        default=None, null=True,
        blank=True,
        to_field='motor_model_number'
    )

    def __str__(self):
        return self.serial_number


class Report(models.Model):
    date_report = models.DateField(null=True)
    # The 'client' field will be created as 'client_id' in the database because of the foreignkey
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
    )
    # The 'motor_serial_number' field will be created as 'motor_serial_number_id' in the database because of the
    # foreignkey
    motor_serial_number = models.ForeignKey(
        MotorOwner,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
    )
    info = models.CharField(max_length=255, default=default_char, blank=True)
    extras = models.TextField(blank=True, null=True)
    exported = models.BooleanField(default=False)
    invoiced = models.BooleanField(default=False)

    def get_motor_owner(self):
        try:
            motor_owner = MotorOwner.objects.get(serial_number=self.motor_serial_number)
            return motor_owner
        except MotorOwner.DoesNotExist:
            return None

    def get_motor_model(self):
        motor_owner = self.get_motor_owner()
        if motor_owner:
            return motor_owner.motor_model
        return None

    def get_client_id(self):
        motor_owner = self.get_motor_owner()
        if motor_owner:
            return motor_owner.client_id
        return None

    def get_sparkplug_model(self):
        motor_model = self.get_motor_model()
        if motor_model:
            try:
                sparkplug = SparkPlug.objects.get(motor_model=motor_model)
                return sparkplug.sparkplug_model
            except SparkPlug.DoesNotExist:
                return None
        return None


# An item can be a task or a material
class Item(models.Model):
    ref = models.CharField(max_length=150, primary_key=True)
    label = models.CharField(max_length=150, default=default_char)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    stock_quantity = models.SmallIntegerField(null=True, blank=True, default=0)


# Each report has multiple items (task or material), for each item correspond a quantity
class ReportItem(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        default=None,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        default=None,
    )
    report_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    class Meta:
        # Enforce uniqueness on the combination of report and item
        unique_together = ('report', 'item')


class Invoice(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT, to_field='id')
    # total_work_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # total_material_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
