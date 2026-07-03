from django.urls import path
from . import views


app_name = "data_visualization"
urlpatterns=[
    path("home", views.home, name='home'),
    path("visualization_type",views.visualization_type,name='visualization_type'),
    path("tables_home",views.tables_home, name='tables_home'),
    path('view_bp',views.view_bp,name='view_bp'),
    path('view_weight',views.view_weight,name='view_weight'),
    path('view_sugar',views.view_sugar,name='view_sugar'),
    path('view_temperature',views.view_temperature,name='view_temperature'),
    path('view_exercise',views.view_exercise,name='view_exercise'),
    path('view_sleep',views.view_sleep,name='view_sleep'),
    path('view_stress',views.view_stress,name='view_stress'),
    path('view_pulse',views.view_pulse,name='view_pulse'),
    path("choose_option",views.choose_option,name='choose_option'),
    path("visualize_systolic_BP",views.visualize_systolic_BP,name='visualize_systolic_BP'),
    path("visualize_diastolic_BP",views.visualize_diastolic_BP,name='visualize_diastolic_BP'),
    path("visualize_weight",views.visualize_weight ,name= 'visualize_weight'),
    path("visualize_blood_sugar",views.visualize_blood_sugar,name='visualize_blood_sugar'),
    path("visualize_temperature",views.visualize_temperature,name='visualize_temperature'),
    path("visualize_pulse",views.visualize_pulse,name='visualize_pulse'),
    path("visualize_exercise",views.visualize_exercise,name='visualize_exercise'),
    path("visualize_sleep",views.visualize_sleep,name='visualize_sleep'),
    path("visualize_stress",views.visualize_stress,name='visualize_stress'),
    path("cumulative_plot",views.cumulative_plot,name='cumulative_plot'),


]