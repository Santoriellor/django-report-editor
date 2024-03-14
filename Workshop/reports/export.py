import os

import pandas as pd
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Report, Client

EXPORT_FOLDER = 'exports'


def export_data(report_id):

    report = get_object_or_404(Report, pk=report_id)
    client = get_object_or_404(Client, pk=report.client.pk)
    fullname = client.last_name + " " + client.first_name
    data = {
        "nom": fullname,
        "téléphone": client.phone_number1,
        "rapport": report.id,
        "moteur": report.motor_serial_number,
    }
    print(data)
    # Export data to PDF
    # pdf_path = generate_pdf_report(data)
    # Export data to XLS
    # xls_path = export_to_xls(data)
    # return render(request, 'export_done.html', {'pdf_path': pdf_path, 'xls_path': xls_path})


def ensure_export_folder_exists():
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)


def generate_pdf_report(data):
    ensure_export_folder_exists()
    # Generate PDF report
    report_path = EXPORT_FOLDER + '/database_report.pdf'
    c = canvas.Canvas(report_path, pagesize=letter)
    c.drawString(100, 750, "Data from Database:")
    y = 730
    for item in data:
        y -= 20
        c.drawString(100, y, f"ID: {item.rapport}, Name: {item.nom}, Email: {item.moteur}")
    c.save()
    return report_path


def export_to_xls(data):
    # Export data to XLS
    xls_path = 'database_data.xlsx'
    df = pd.DataFrame([(item.id, item.name, item.email) for item in data], columns=['ID', 'Name', 'Email'])
    df.to_excel(xls_path, index=False)
    return xls_path
