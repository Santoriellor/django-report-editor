from django.contrib import admin
from .models import (Client, Report, Invoice, SparkPlug,
                     OilFilter, FuelFilter, Impeller, MotorModel,
                     Item, ReportItem, MotorOwner)

# Register your models here.
admin.site.register(Client)
admin.site.register(Report)
admin.site.register(Invoice)
admin.site.register(SparkPlug)
admin.site.register(OilFilter)
admin.site.register(FuelFilter)
admin.site.register(Impeller)
admin.site.register(MotorModel)
admin.site.register(Item)
admin.site.register(ReportItem)
admin.site.register(MotorOwner)
