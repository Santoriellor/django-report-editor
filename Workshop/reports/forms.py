from datetime import date
from django import forms
from django.core.validators import RegexValidator
from django.forms import BoundField
from django.utils.translation import gettext_lazy as _
from .models import Report, Client, MotorOwner, MotorModel, Item, ReportItem


class ReportForm(forms.ModelForm):
    # Get instances of Client to use as choices
    clients = Client.objects.all()
    # Create a list of tuples where the first element is the instance itself
    # and the second element is the attribute you want to display (e.g., name)
    choices = [(client, client.last_name) for client in clients]
    # Overide the field data from meta (and models)
    # Define your choice field with the customized choices
    # When you change the empty_label parameter, you must update the script to render the motr select disabled
    client = forms.ModelChoiceField(
        queryset=clients,
        empty_label=_("Choisir un client"),
        label=_("Nom du client"),
    )

    class Meta:
        model = Report
        # fields = ['date_report', 'client', 'motor_serial_number', 'info']
        fields = '__all__'
        exclude = ['exported']
        labels = {
            "date_report": _("Date de création"),
            "motor_serial_number": _("N° de série moteur"),
            "info": _("Informations diverses"),
        }
        widgets = {
            "date_report": forms.DateInput(attrs={"style": "width: 140px; padding: 2px; border-radius: 5px; border: solid 1px #dee2e6; text-align: center;"}),
            "info": forms.Textarea(attrs={
                "rows": 4,
                "style": "width: 100%; resize: none; padding: 5px; border-radius: 5px; border: solid 1px var(--border-color1);"
            }),
        }

    def __init__(self,  *args, **kwargs):
        report_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Initialize the date_report field with the current date
        self.fields['date_report'].initial = date.today()
        # Disabled the date_report field
        self.fields['date_report'].disabled = True

        self.fields['client'].widget.attrs["style"] = "width:  140px; padding: 2px; border-radius: 5px; border: solid 1px var(--border-color1);"
        self.fields['motor_serial_number'].widget.attrs["style"] = "width:  140px; padding: 2px; border-radius: 5px; border: solid 1px var(--border-color1);"

        # Query all items from the Item model
        items = Item.objects.all()

        # Dynamically add form fields for each item
        for item in items:
            field_name = f'item_{item.pk}'  # Construct a unique field name for each item

            # if the item is a task, add a checkbox to the form (boolean)
            if field_name.startswith('item_task'):
                self.fields[field_name] = forms.BooleanField(
                    label=item.label,
                    required=False,  # Make the field optional
                    widget=forms.CheckboxInput(attrs={
                        'style': 'vertical-align: middle; margin: 0; padding: 0; cursor: pointer; outline: none; border: 1px solid var(--border-color1);'}),
                )
            # if the item is a material, add a decimal field to the form (quantity)
            elif field_name.startswith('item_material'):
                self.fields[f"{field_name}_qty"] = forms.DecimalField(
                    label=item.label,
                    required=False,
                    widget=forms.NumberInput(attrs={'style': 'width: calc(1.9rem + 2vw); var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);'}),
                )

        # Populate initial data for item fields if instance exists
        if report_instance:
            # Retrieve the associated ReportItem instances for the report
            report_items = ReportItem.objects.filter(report=report_instance)
            # Create a dictionary to hold initial data for the form
            initial_data = {}
            # Populate initial data for item fields based on associated ReportItem instances
            for report_item in report_items:
                if report_item.item.pk.startswith('task'):
                    initial_data[f'item_{report_item.item.pk}'] = True
                elif report_item.item.pk.startswith('material'):
                    initial_data[f'item_{report_item.item.pk}_qty'] = report_item.report_quantity
            # Set initial data for the form
            self.initial.update(initial_data)
            # Populate initial data for other fields if instance exists
            self.initial['client'] = report_instance.client.id  # Assuming client is a ForeignKey
            self.initial['info'] = report_instance.info


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'phone_number1', 'phone_number2', 'address', 'email', 'client_info']

        labels = {
            "last_name": _("Nom"),
            "first_name": _("prénom"),
            "client_info": _("Informations diverses"),
            "phone_number1": _("Téléphone n°1"),
            "phone_number2": _("Téléphone n°2"),
            "address": _("Adresse"),
            "email": _("Adresse email"),
        }
        widgets = {
            "last_name": forms.TextInput(attrs={"style": "width: 150px; padding: 2px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"}),
            "first_name": forms.TextInput(attrs={"style": "width: 150px; padding: 2px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"}),
            "phone_number1": forms.TextInput(attrs={"style": "width: 150px; padding: 2px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"}),
            "phone_number2": forms.TextInput(attrs={"style": "width: 150px; padding: 2px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"}),
            "email": forms.EmailInput(attrs={"style": "width: 150px; padding: 2px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"}),
            "client_info": forms.Textarea(attrs={
                "rows": 4,
                "style": "width: 100%; resize: none; padding: 5px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"
            }),
            "address": forms.Textarea(attrs={
                "rows": 2,
                "style": "width: 100%; resize: none; padding: 5px; var(--font-size); border-radius: 5px; border: solid 1px var(--border-color1);"
            }),
        }
        # validators = {
        #     "phone_number1": [RegexValidator(
        #         regex=r"",
        #         message='Enter a valid telephone number',
        #         code='invalid_format'
        #     )]
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

