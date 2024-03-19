from .models import Item

tasks = [
    ('task_accessory_motor', 15, 30),
    ('task_accessory_fueltank', 15, 30),
    ('task_accessory_fuelhose', 15, 30),
    ('task_accessory_boatlicense', 15, 30),
]


def fill_item():
    for task, price, stock_quantity in tasks:
        item = Item(ref=task, price=price, stock_quantity=stock_quantity)
        item.save()

# task_accessory_AWD
# task_accessory_inspectionreport
# task_accessory_pickup
# task_accessory_receipt
# task_boat_transport
# task_boat_to_storage
# task_boat_out_of_storage
# task_boat_hauling_out
# task_boat_launching
# task_boat_bilge
# task_boat_hull_cleaning
# task_boat_hull_decalcify
# task_boat_hull_sand
# task_boat_hull_paint
# task_boat_deck_cleaning
# task_boat_cockpit_cleaning
# task_motor_dismount
# task_motor_mount
# task_motor_pick_up
# task_motor_return
# task_motor_cleaning
# task_motor_dismantle
# task_shaft_cleaning
# task_shaft_dismantle
# task_gearbox_cleaning
# task_gearbox_dismantle
# task_anode_replace
# task_motor_oil_replace
# task_gearbox_oil_replace
# task_greasing_points
# task_carburetor_cleaning
# task_carburetor_setting
# task_carburetor_revise
# task_fuelfilter_cleaning
# task_fuelfilter_replace
# task_fueltank_cleaning
# task_oilfilter_replace
# task_ignition_testing
# task_ignition_setting
# task_ignition_repair
# task_sparkplug_control
# task_sparkplug_replace
# task_computer_diagnosis
# task_waterpump_testing
# task_impeller_replace
# task_starter_testing
# task_starter_repair
# task_compression_testing
# task_pressure_loss_testing
# task_valves_testing
# task_valves_setting
# task_thermostat_testing
# task_thermostat_replace
# task_gearbox_disassemble
# task_gearbox_testing
# task_gearbox_repair
# task_gearbox_sealoff
# task_propeller_dismantle
# task_propeller_repair
# task_propeller_replace
# task_battery_testing
# task_battery_charging
# task_battery_remove
# task_battery_install
# task_battery_replace
# task_testrun
# task_testdrive
# task_motor_winterizing
# task_perform_Abgaswartung
# material_motor_oil
# material_gearbox_oil
# material_cleaning
# material_sparkplug
# material_fuelhose
# material_oring
# material_impeller
# material_carburetor_seal
# material_pins
# material_seals
# material_shear_pin
# material_oilfilter
# material_fuelfilter
# material_fuel_additive
# material_descaling_agent
# material_thermostat
# material_propeller
# material_battery
# material_VRG_battery
# material_emission_inspection_document
# material_computer_diagnosis
# material_crane
# material_boat_winter_storage
# material_motor_winter_storage
# material_work_hour