from django.urls import path
from . import views

app_name= "notifications"

urlpatterns=[
    path("home/", views.home, name='home'),
    path("<int:notification_id>/read/", views.mark_as_read, name='mark_as_read'),
]