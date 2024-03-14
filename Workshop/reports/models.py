from django.db import models

# By default, Django automatically adds an integer primary key field to each model, called id
# By default, integer fields in Django models are auto-incremented.
# If blank=True then the form field will be required=False, else required=True

default_char = ''


# Create your models here.
class Client(models.Model):
    last_name = models.CharField(max_length=50, default=default_char)
    first_name = models.CharField(max_length=50, default=default_char)
    phone_number1 = models.CharField(max_length=20, default=default_char)
    phone_number2 = models.CharField(max_length=20, default=default_char, blank=True)
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
    info = models.CharField(max_length=50, default=default_char, blank=True)
    accessory_motor = models.BooleanField(default=False)
    accessory_fueltank = models.BooleanField(default=False)
    accessory_fuelhose = models.BooleanField(default=False)
    accessory_boatlicense = models.BooleanField(default=False)
    accessory_AWD = models.BooleanField(default=False)
    accessory_inspectionreport = models.BooleanField(default=False)
    accessory_pickup = models.BooleanField(default=False)
    accessory_receipt = models.BooleanField(default=False)
    boat_transport = models.BooleanField(default=False)
    boat_to_storage = models.BooleanField(default=False)
    boat_out_of_storage = models.BooleanField(default=False)
    boat_hauling_out = models.BooleanField(default=False)
    boat_launching = models.BooleanField(default=False)
    boat_bilge = models.BooleanField(default=False)
    boat_hull_cleaning = models.BooleanField(default=False)
    boat_hull_decalcify = models.BooleanField(default=False)
    boat_hull_sand = models.BooleanField(default=False)
    boat_hull_paint = models.BooleanField(default=False)
    boat_deck_cleaning = models.BooleanField(default=False)
    boat_cockpit_cleaning = models.BooleanField(default=False)
    motor_dismount = models.BooleanField(default=False)
    motor_mount = models.BooleanField(default=False)
    motor_pick_up = models.BooleanField(default=False)
    motor_return = models.BooleanField(default=False)
    motor_cleaning = models.BooleanField(default=False)
    motor_dismantle = models.BooleanField(default=False)
    shaft_cleaning = models.BooleanField(default=False)
    shaft_dismantle = models.BooleanField(default=False)
    gearbox_cleaning = models.BooleanField(default=False)
    gearbox_dismantle = models.BooleanField(default=False)
    anode_replace = models.BooleanField(default=False)
    motor_oil_replace = models.BooleanField(default=False)
    gearbox_oil_replace = models.BooleanField(default=False)
    greasing_points = models.BooleanField(default=False)
    carburetor_cleaning = models.BooleanField(default=False)
    carburetor_setting = models.BooleanField(default=False)
    carburetor_revise = models.BooleanField(default=False)
    fuelfilter_cleaning = models.BooleanField(default=False)
    fuelfilter_replace = models.BooleanField(default=False)
    fueltank_cleaning = models.BooleanField(default=False)
    oilfilter_replace = models.BooleanField(default=False)
    ignition_testing = models.BooleanField(default=False)
    ignition_setting = models.BooleanField(default=False)
    ignition_repair = models.BooleanField(default=False)
    sparkplug_control = models.BooleanField(default=False)
    sparkplug_replace = models.BooleanField(default=False)
    computer_diagnosis = models.BooleanField(default=False)
    waterpump_testing = models.BooleanField(default=False)
    impeller_replace = models.BooleanField(default=False)
    starter_testing = models.BooleanField(default=False)
    starter_repair = models.BooleanField(default=False)
    compression_testing = models.BooleanField(default=False)
    pressure_loss_testing = models.BooleanField(default=False)
    valves_testing = models.BooleanField(default=False)
    valves_setting = models.BooleanField(default=False)
    thermostat_testing = models.BooleanField(default=False)
    thermostat_replace = models.BooleanField(default=False)
    gearbox_disassemble = models.BooleanField(default=False)
    gearbox_testing = models.BooleanField(default=False)
    gearbox_repair = models.BooleanField(default=False)
    gearbox_sealoff = models.BooleanField(default=False)
    propeller_dismantle = models.BooleanField(default=False)
    propeller_repair = models.BooleanField(default=False)
    propeller_replace = models.BooleanField(default=False)
    battery_testing = models.BooleanField(default=False)
    battery_charging = models.BooleanField(default=False)
    battery_remove = models.BooleanField(default=False)
    battery_install = models.BooleanField(default=False)
    battery_replace = models.BooleanField(default=False)
    testrun = models.BooleanField(default=False)
    testdrive = models.BooleanField(default=False)
    motor_winterizing = models.BooleanField(default=False)
    perform_Abgaswartung = models.BooleanField(default=False)
    motor_oil_qty = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # motor_oil_liter_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    gearbox_oil_qty = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # gearbox_oil_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cleaning_material_qty = models.SmallIntegerField(null=True, blank=True)
    # cleaning_material_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sparkplug_qty = models.SmallIntegerField(null=True, blank=True)
    # sparkplug_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fuelhose_qty = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # fuelhose_meter_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    oring_qty = models.SmallIntegerField(null=True, blank=True)
    # oring_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    impeller_qty = models.SmallIntegerField(null=True, blank=True)
    # impeller_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    carburetor_seal_qty = models.SmallIntegerField(null=True, blank=True)
    # carburetor_seal_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    pins_qty = models.SmallIntegerField(null=True, blank=True)
    # pins_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    seals_qty = models.SmallIntegerField(null=True, blank=True)
    # seals_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    shear_pin_qty = models.SmallIntegerField(null=True, blank=True)
    # shear_pin_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    oilfilter_qty = models.SmallIntegerField(null=True, blank=True)
    # oilfilter_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fuelfilter_qty = models.SmallIntegerField(null=True, blank=True)
    # fuelfilter_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fuel_additive_qty = models.SmallIntegerField(null=True, blank=True)
    # fuel_additive_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    descaling_agent_qty = models.SmallIntegerField(null=True, blank=True)
    # descaling_agent_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    thermostat_qty = models.SmallIntegerField(null=True, blank=True)
    # thermostat_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    propeller_qty = models.SmallIntegerField(null=True, blank=True)
    # propeller_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    battery_qty = models.SmallIntegerField(null=True, blank=True)
    # battery_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    VRG_battery_qty = models.SmallIntegerField(null=True, blank=True)
    # VRG_battery_unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    emission_inspection_document_qty = models.SmallIntegerField(null=True, blank=True)
    # emission_inspection_document_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    computer_diagnosis_qty = models.SmallIntegerField(null=True, blank=True)
    # computer_diagnosis_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # auto_flat_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # emission_inspection_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # cleaning_flat_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # tansport_flat_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    crane_qty = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # crane_hour_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    boat_winter_storage_square_meter = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # boat_winter_storage_square_meter_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    motor_winter_storage_qty = models.SmallIntegerField(null=True, blank=True)
    # motor_winter_storage_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    work_hour_qty = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # work_hour_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_work_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_material_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    extras = models.TextField(blank=True, null=True)
    exported = models.BooleanField(default=False)

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


class PriceRef(models.Model):
    ref = models.CharField(max_length=150, primary_key=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class Invoice(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT, to_field='id')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
