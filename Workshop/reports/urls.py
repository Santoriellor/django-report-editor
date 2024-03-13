from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.new_report, name="new_report"),
    path("read/", views.read_report, name="read_report"),
    path("list_reports/", views.list_reports, name="list_reports"),
    path("exported_reports/", views.exported_reports, name="exported_reports"),
    path("new_client/", views.new_client, name="new_client"),
    path("update_client/", views.update_client, name="update_client"),
    path('get_motors/', views.get_motors, name='get_motors'),
    path('get_motor_data/', views.get_motor_data, name='get_motor_data'),
]
