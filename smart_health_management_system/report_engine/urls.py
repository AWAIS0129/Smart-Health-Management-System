from django.urls import path
from . import views


app_name = 'report_engine'
urlpatterns = [
    path("", views.report_home, name='home'),
    path("generate/", views.generate_report, name='generate_report'),
    path("export_csv",views.export_csv, name= 'export_csv'),
]
