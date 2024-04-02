import json
import os

from django.shortcuts import get_object_or_404
from .models import Report, Client, ReportItem, Item

EXPORT_FOLDER = 'exports'
JSON_FOLDER = 'json'


def export_data(report_id):
    # Retrieve report and client information
    report = get_object_or_404(Report, pk=report_id)
    client = get_object_or_404(Client, pk=report.client.pk)
    fullname = f"{client.last_name} {client.first_name}"

    # Retrieve report items
    report_items = ReportItem.objects.filter(report=report)

    # Calculate subtotal and tax amount
    subtotal = float(sum(report_item.item.price * report_item.report_quantity for report_item in report_items))
    tax_rate = 0.1
    tax_amount = float(subtotal) * tax_rate

    # Prepare data dictionary
    data = {
        "invoice_number": report_id,
        "date": report.date_report.isoformat(),
        "customer": {
            "name": fullname,
            "email": client.email,
            "address": client.address,
        },
        "items": [],
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "total": subtotal + tax_amount,
    }

    # Add each report item to the items list
    for report_item in report_items:
        item = report_item.item
        item_data = {
            "description": item.label,
            "reference": item.ref,
            "quantity": float(report_item.report_quantity),
            "unit_price": float(item.price),
            "total": float(item.price * report_item.report_quantity),
        }
        data["items"].append(item_data)

    # Call function to create JSON file
    create_json(data, report_id, report.date_report)


def ensure_export_folder_exists():
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)


def ensure_json_folder_exists():
    if not os.path.exists(JSON_FOLDER):
        os.makedirs(JSON_FOLDER)


def create_json(data, report_id, date):
    ensure_json_folder_exists()
    # Write data to JSON file
    with open(f'{JSON_FOLDER}/{date}_report_{report_id}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        return True

