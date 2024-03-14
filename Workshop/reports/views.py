from django.db import connection
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import ReportForm, ClientForm
from .invoice_calculator import invoice_calculator
from .models import Report, Client, MotorOwner, MotorModel

# for testing purpose
import win32api
# testsequence
# def show_alert(title, message):
#     win32api.MessageBox(0, message, title, 0x00001000)
#
# show_alert("Alert", f"no save")
# endtestsequence


# Create your views here.
# Show the selected report
def read_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    client = get_object_or_404(Client, pk=report.client_id)
    return render(request, 'read_report.html', {'report': report, 'client': client})


def update_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()  # Update the existing instance
            return redirect('list_reports')  # Redirect to 'list_reports'
    else:
        form = ReportForm(instance=report)
    return render(request, 'new_report.html', {'form': form})


def delete_report(request, id):
    pass


def export_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    report.exported = True
    report.save()
    return redirect('list_exported')


def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_reports')  # Redirect to 'list_reports'
        else:
            pass
    else:
        form = ReportForm()
    return render(request, 'new_report.html', {'form': form})


def list_reports(request):
    # Run a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reports_report WHERE exported = 0")
        rows = cursor.fetchall()
        report_links = []
        for row in rows:
            client_id = row[134]
            if client_id:
                report = get_object_or_404(Report, pk=row[0])
                client = get_object_or_404(Client, pk=client_id)
                text_report = report.date_report.strftime('%m/%d/%Y') + " - Rapport n°" + str(report.id) + " - " + client.last_name.capitalize()
                url_read = reverse('read_report', kwargs={'report_id': report.id})
                url_update = reverse('update_report', kwargs={'report_id': report.id})
                url_export = reverse('export_report', kwargs={'report_id': report.id})
                row_str = f"<a href='{url_read}'>{text_report}</a> - <a href='{url_update}'><button type='button'>Modifier</button></a> - <a href='{url_export}'><button type='button'>Exporter</button></a>"
                report_links.append(row_str)
    # Pass the report_links list as a context variable
    context = {'report_links': report_links}
    return render(request, 'list_report.html', context)


def list_exported(request):
    # Run a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reports_report WHERE exported = 1")
        rows = cursor.fetchall()
        report_links = []
        for row in rows:
            client_id = row[134]
            if client_id:
                report = get_object_or_404(Report, pk=row[0])
                client = get_object_or_404(Client, pk=client_id)
                text_report = report.date_report.strftime('%m/%d/%Y') + " - Rapport n°" + str(
                    report.id) + " - " + client.last_name.capitalize()
                url_export_pdf = reverse('export_report_pdf', kwargs={'report_id': report.id})
                row_str = f"{text_report} - <a href='{url_export_pdf}'><button type='button'>Export PDF</button></a>"
                report_links.append(row_str)
    # Pass the report_links list as a context variable
    context = {'report_links': report_links}
    return render(request, 'list_exported.html', context)


def export_report_pdf(request, report_id):
    invoice_calculator(report_id)
    return redirect('list_exported')


def new_client(request):
    if request.method == 'POST':
        # Creating a form to change an existing article.
        # >> > article = Article.objects.get(pk=1)
        # >> > form = ArticleForm(instance=article)
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_report')  # Redirect to 'new_report' URL
    else:
        if request.GET.get('list_client_id'):
            client_id = request.GET.get('list_client_id')
            client = Client.objects.get(pk=client_id)
            form = ClientForm(instance=client)
        else:
            form = ClientForm()
    return render(request, 'new_client.html', {'form': form})


def list_client(request):
    # Run a raw SQL query
    with (connection.cursor() as cursor):
        cursor.execute("SELECT * FROM reports_client")
        rows = cursor.fetchall()
        client_links = []
        for row in rows:
            client_id = row[0]
            client = get_object_or_404(Client, pk=client_id)
            text_client = client.last_name.capitalize() + " " + client.first_name.capitalize()
            text_client += " - tél. " + client.phone_number1
            url_update = reverse('new_client') + f"?list_client_id={client.id}"
            url_new = reverse('new_client') + f"?infos_client={client_id}"
            row_str = f"<a href='{url_new}'>{text_client}</a> - <a href='{url_update}'><button type='button'>Modifier</button></a>"
            client_links.append(row_str)
    # Pass the client_links list as a context variable
    context = {'client_links': client_links}
    return render(request, 'list_client.html', context)


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
