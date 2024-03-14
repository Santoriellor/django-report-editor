from datetime import date
from django import forms
from django.forms import BoundField
from django.utils.translation import gettext_lazy as _
from .models import Report, Client, MotorOwner, MotorModel


class ReportForm(forms.ModelForm):
    # Get instances of Client to use as choices
    clients = Client.objects.all()

    # Create a list of tuples where the first element is the instance itself
    # and the second element is the attribute you want to display (e.g., name)
    choices = [(client, client.last_name) for client in clients]

    # Overide the field data from meta (and models)
    # Define your choice field with the customized choices
    # When you change the empty_label parameter, you must update the script to render the motr select disabled
    client = forms.ModelChoiceField(queryset=clients, empty_label=_("Choisir un client"))

    class Meta:
        model = Report
        # fields = ['date_report', 'client', 'motor_serial_number', 'info', 'accessory_motor']
        fields = '__all__'
        exclude = ['exported']
        labels = {
            "date_report": _("Date de création"),
            "motor_serial_number": _("Numéro de série du moteur"),
            "info": _("Informations diverses"),
            "accessory_motor": _("Moteur"),
        }
        widgets = {
            # "date_report": forms.DateField(attrs={'readonly': True}),
            "info": forms.Textarea(attrs={"rows": 4, "style": "width: 100%; resize: none; padding: 5px;"}),
            # "accessory_motor": forms.CheckboxInput(),
        }
        # help_texts = {
        #     "name": _("Some useful help text."),
        # }
        # error_messages = {
        #     "name": {
        #         "max_length": _("This writer's name is too long."),
        #     }

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the date_report field with the current date
        self.fields['date_report'].initial = date.today()
        # Disabled the date_report field
        self.fields['date_report'].disabled = True

    def grouped_fields(self):
        grouped = {}
        for name, field in self.fields.items():
            bf = BoundField(self, field, name)
            if name.startswith("accessory_"):
                group_name = "accessoires"
            elif name.startswith("boat_"):
                group_name = "bateau"
            elif name.startswith("motor_") and name != "motor_serial_number":
                group_name = "moteur"
            else:
                group_name = None

            if group_name is not None:
                grouped.setdefault(group_name, []).append(bf)
        return grouped


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'phone_number1', 'phone_number2', 'address', 'email', 'client_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['client_info'] = forms.CharField(widget=forms.Textarea, required=False)
