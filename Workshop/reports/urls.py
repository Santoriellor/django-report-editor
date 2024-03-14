from django.urls import path

from . import views

urlpatterns = [
    path("new_report/", views.new_report, name="new_report"),
    path("update_report/<int:report_id>/", views.update_report, name="update_report"),
    path("export_report/<int:report_id>/", views.export_report, name="export_report"),
    path("export_report_pdf/<int:report_id>/", views.export_report_pdf, name="export_report_pdf"),
    path("read_report/<int:report_id>/", views.read_report, name="read_report"),
    path("list_reports/", views.list_reports, name="list_reports"),
    path("list_exported/", views.list_exported, name="list_exported"),
    path("new_client/", views.new_client, name="new_client"),
    # path("update_client/", views.update_client, name="update_client"),
    path("list_client/", views.list_client, name="list_client"),
    path('get_motors/', views.get_motors, name='get_motors'),
    path('get_motor_data/', views.get_motor_data, name='get_motor_data'),
]
