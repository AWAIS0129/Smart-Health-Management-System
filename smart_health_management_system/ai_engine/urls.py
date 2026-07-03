from django.urls import path
from . import views

app_name = "ai_engine"

urlpatterns = [
    path("home/",views.home, name= 'home'),
    path("infer/", views.infer, name='infer'),
]
