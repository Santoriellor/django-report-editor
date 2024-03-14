from django.forms import model_to_dict

from .models import Report

my_object = Report.objects.get(id=1)
# data_dict = model_to_dict(my_object)
# print(data_dict)
