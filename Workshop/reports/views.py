import os
from pathlib import Path

from django.db import connection
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .export import export_data
from .forms import ReportForm, ClientForm
from .models import Report, Client, MotorOwner, MotorModel, ReportItem, Item


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
def fill_table(request):
    # fill_item()
    return redirect('list_reports')


def home(request):
    return render(request, 'reports/home.html')


def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # Save the report instance to get its primary key
            report_instance = form.save()

            # Iterate through the form fields
            for field_name, field_value in form.cleaned_data.items():
                # Check if the field corresponds to an item
                if field_name.startswith('item_') and field_value:
                    # Get the item ID from the field name
                    item_id = field_name[5:]
                    # Fetch the Item instance
                    if item_id.startswith('task'):
                        item_instance = Item.objects.get(pk=item_id)
                        qty_instance = 1
                    elif item_id.startswith('material'):
                        item_instance = Item.objects.get(pk=item_id[:-4])
                        qty_instance = field_value
                    # Create a new ReportItem instance
                    ReportItem.objects.create(
                        report=report_instance,
                        item=item_instance,
                        report_quantity=qty_instance)

            return redirect('list_reports')
    else:
        form = ReportForm()
    return render(
        request,
        'reports/new_report.html',
        {
            'form': form,
        })


def update_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)

        if form.is_valid():
            report_instance = form.save()  # Update the existing instance

            # Iterate through the form fields
            for field_name, field_value in form.cleaned_data.items():
                # Check if the field corresponds to an item
                if field_name.startswith('item_'):
                    # Get the item ID from the field name
                    item_id = field_name[5:]
                    # Fetch the Item instance
                    if item_id.startswith('task'):
                        item_instance = Item.objects.get(pk=item_id)
                        qty_instance = 1
                    elif item_id.startswith('material'):
                        item_instance = Item.objects.get(pk=item_id[:-4])
                        qty_instance = field_value
                    # Check if the item is selected in the form
                    if field_value:
                        # Create or update a ReportItem instance
                        try:
                            # Try to retrieve the existing instance
                            report_item_instance = ReportItem.objects.get_or_create(
                                report=report_instance,
                                item=item_instance,
                                report_quantity=qty_instance
                            )
                        except IntegrityError:
                            # If a duplicate entry is encountered, update the existing instance
                            report_item_instance = ReportItem.objects.filter(
                                report=report_instance,
                                item=item_instance
                            ).first()
                            if report_item_instance:
                                # Update the existing instance's attributes as needed
                                report_item_instance.report_quantity = qty_instance
                                report_item_instance.save()
                    else:
                        # Delete the ReportItem instance if the item is not selected
                        ReportItem.objects.filter(report=report_instance, item=item_instance).delete()
            return redirect('list_reports')  # Redirect to 'list_reports'
    else:
        form = ReportForm(instance=report)

    return render(
        request,
        'reports/new_report.html',
        {
            'form': form,
        })


def delete_report(request, report_id):
    # Run a raw SQL query
    report_instance = Report.objects.get(pk=report_id)
    report_items = ReportItem.objects.filter(report=report_instance)
    report_items.delete()  # or report_items.update(report=None)
    report_instance.delete()
    return redirect('list_reports')


def export_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    report.exported = True
    report.save()
    return redirect('list_exported')


def read_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    client = get_object_or_404(Client, pk=report.client_id)
    # Filter items where the name starts with "task"
    task_items = Item.objects.filter(ref__startswith='task')
    # Filter items where the name starts with "material"
    material_items = Item.objects.filter(ref__startswith='material')
    # Filter report items corresponding to the task items
    tasks = ReportItem.objects.filter(report=report_id, item__in=task_items)
    # Filter report items corresponding to the material items
    materials = ReportItem.objects.filter(report=report_id, item__in=material_items)
    return render(request, 'reports/read_report.html', {'report': report, 'client': client, 'tasks': tasks, 'materials': materials})


def list_reports(request):
    # Run a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reports_report WHERE exported = 0")
        rows = cursor.fetchall()
        report_links = []
        if len(rows) == 0:
            report_links.append("<p>Il n'y a pas de rapports commencés.</p>")
        else:
            for row in rows:
                client_id = row[5]
                if client_id:
                    report = get_object_or_404(Report, pk=row[0])
                    client = get_object_or_404(Client, pk=client_id)
                    text_report = report.date_report.strftime('%m/%d/%Y')
                    text_report += " - Rapport n°" + str(report.id) + "<br>"
                    text_report += client.last_name.capitalize()
                    url_read = reverse('read_report', kwargs={'report_id': report.id})
                    url_update = reverse('update_report', kwargs={'report_id': report.id})
                    url_delete = reverse('delete_report', kwargs={'report_id': report.id})
                    url_export = reverse('export_report', kwargs={'report_id': report.id})
                    row_str = "<div class='card'>"
                    row_str += f"<div class='item1'>{text_report}</div>"
                    row_str += f"<div class='buttons'><a href='{url_read}'>Consulter</a>"
                    row_str += f"<a href='{url_update}'>Modifier</a>"
                    row_str += f"</div><div class='buttons'><a href='{url_delete}' class='delete-link'>Supprimer</a>"
                    row_str += f"<a href='{url_export}'>Exporter</a></div>"
                    row_str += "</div>"
                    report_links.append(row_str)
    # Pass the report_links list as a context variable
    context = {'report_links': report_links}
    return render(request, 'reports/list_report.html', context)


def list_exported(request):
    # Run a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reports_report WHERE exported = 1 AND invoiced = 0")
        rows = cursor.fetchall()
        report_links = []
        if len(rows) == 0:
            report_links.append("<p>Il n'y a pas de rapports exportés.</p>")
        else:
            for row in rows:
                client_id = row[5]
                if client_id:
                    report = get_object_or_404(Report, pk=row[0])
                    client = get_object_or_404(Client, pk=client_id)
                    text_report = report.date_report.strftime('%m/%d/%Y') + " - Rapport n°" + str(
                        report.id) + " - " + client.last_name.capitalize()
                    url_read = reverse('read_report', kwargs={'report_id': report.id})
                    url_export_pdf = reverse('export_report_pdf', kwargs={'report_id': report.id})
                    row_str = "<div class='card'>"
                    row_str += f"<div class='item1'>{text_report}</div>"
                    row_str += f"<div class='buttons'><a href='{url_read}'>Consulter</a>"
                    row_str += f"<a href='{url_export_pdf}'>Facture</a></div>"
                    row_str += "</div>"
                    report_links.append(row_str)
    # Pass the report_links list as a context variable
    context = {'report_links': report_links}
    return render(request, 'reports/list_exported.html', context)


def list_invoice(request):
    # Specify the directory path
    directory = os.path.join(BASE_DIR, "json/")
    # Get the list of files in the directory
    files = os.listdir(directory)
    invoice_links = []
    for file in files:
        row_str = "<div class='row'>"
        row_str += f"<div class='item1'><a href='{file}'>{file}</a></div>"
        row_str += "</div>"
        invoice_links.append(row_str)
    # Pass the list of files to the template context
    return render(request, 'reports/list_invoice.html', {'invoice_links': invoice_links})


def export_report_pdf(request, report_id):
    export_data(report_id)
    report = Report.objects.get(pk=report_id)
    report.invoiced = True
    report.save()
    return redirect('list_exported')


def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_client')
    else:
        form = ClientForm()
    return render(request, 'reports/new_client.html', {'form': form})


def update_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()  # Update the existing instance
            return redirect('list_client')  # Redirect to 'list_reports'
    else:
        form = ClientForm(instance=client)
    return render(request, 'reports/new_client.html', {'form': form})


def list_client(request):
    # Run a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reports_client")
        rows = cursor.fetchall()
        client_links = []
        for row in rows:
            client_id = row[0]
            client = get_object_or_404(Client, pk=client_id)
            name_client = client.last_name.capitalize() + " " + client.first_name.capitalize()
            phone_client1 = "Tél. " + client.phone_number1
            phone_client2 = "Tél. " + client.phone_number2
            email_client = "Email : " + client.email
            addr_client = "Adr: " + client.address
            url_new = reverse('new_client') + f"?infos_client={client_id}"
            url_update = reverse('update_client', kwargs={'client_id': client.id})
            row_str = "<div class='card'>"
            row_str += f"<div class='item1'>{name_client}</div>"  # <a href='{url_new}'></a>
            row_str += f"<div class='item2'>{phone_client1} - {phone_client2}</div>"
            row_str += f"<div class='item2'>{email_client}</div>"
            row_str += f"<div class='item2'>{addr_client}</div>"
            row_str += f"<div class='buttons'><a href='{url_update}'>Modifier</a></div>"
            row_str += "</div>"
            client_links.append(row_str)
    # Pass the client_links list as a context variable
    context = {'client_links': client_links}
    return render(request, 'reports/list_client.html', context)


def get_motors(request):
    # Query motor options based on the selected client
    client_id = request.GET.get('client_id')
    motors = MotorOwner.objects.filter(client_id=client_id)
    motor_choices = [{'serial_number': motor.serial_number} for motor in motors]
    return JsonResponse({'motors': motor_choices})


def get_motor_data(request):
    # Query sparkplug options based on the selected motor
    motor_serial_number = request.GET.get('motor_serial_number')
    motor_model = MotorOwner.objects.filter(serial_number=motor_serial_number).values('motor_model_number_id')
    # Access the first item in the queryset
    if motor_model.exists():
        motor_ref = motor_model[0]['motor_model_number_id']
    sparkplug = MotorModel.objects.filter(motor_model_number=motor_ref).values('spark_plug')
    if sparkplug.exists():
        sparkplug_ref = sparkplug[0]['spark_plug']
    oilfilter = MotorModel.objects.filter(motor_model_number=motor_ref).values('oil_filter')
    if oilfilter.exists():
        oilfilter_ref = oilfilter[0]['oil_filter']
    impeller = MotorModel.objects.filter(motor_model_number=motor_ref).values('impeller')
    if impeller.exists():
        impeller_ref = impeller[0]['impeller']
    data_dict = {
        'sparkplug': sparkplug_ref,
        'oilfilter': oilfilter_ref,
        'impeller': impeller_ref
    }
    return JsonResponse(data_dict)
