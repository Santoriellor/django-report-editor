from django.db import models


class ClientFields():
    """ Fields for the Client model """
    # last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    phone_number1 = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    client_info = models.CharField(max_length=255)


class ReportFields():
    """ Fields for the Report model """
    client_id = models.SmallIntegerField()
