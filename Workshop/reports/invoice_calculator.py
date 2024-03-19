from django.shortcuts import get_object_or_404

from .models import Report, Client

# for testing purpose
import win32api


# testsequence
def show_alert(title, message):
    win32api.MessageBox(0, message, title, 0x00001000)
#
# show_alert("Alert", f"no save")
# endtestsequence


def invoice_calculator(report_id):
    # Get the Report
    report = get_object_or_404(Report, pk=report_id)
    client = get_object_or_404(Client, pk=report.client.pk)
    fullname = client.last_name + " " + client.first_name
    price = 0

    # Get all primary keys from the PriceRef model
    priceref_pks = PriceRef.objects.values_list('pk', flat=True)

    # Loop through each field of the Report model
    for field in report._meta.fields:
        # Get the name of the field
        field_name = field.name

        # Check if the field exists in the PriceRef model and its primary key is in priceref_pks
        if field_name in priceref_pks and getattr(report, field_name):
            # Retrieve the corresponding PriceRef instance
            priceref_instance = PriceRef.objects.get(pk=field_name)

            # Add the price from the PriceRef instance to the total price
            price += priceref_instance.price

    show_alert("Alert", f"price = {price}")

    data = {
        "nom": fullname,
        "téléphone": client.phone_number1,
        "rapport": report.id,
        "moteur": report.motor_serial_number,
    }



