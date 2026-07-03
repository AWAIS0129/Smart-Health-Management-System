from django.urls import path
from . import views 


app_name = "dashboard"


urlpatterns= [
    path('main_dashboard/', views.dashboard, name='dashboard'),


]