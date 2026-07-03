from django.urls import path
from . import views

app_name = "health_data_manager"
urlpatterns=[
    path('mode', views.mode, name='mode_selection'),
    path('operations', views.operations,name="operations"),
    path("edit_health_data",views.edit_health_data,name='edit_health_data'),
    path('manual',views.manual_entry, name="manual_health_data_entry"),
    path('file_upload',views.file_upload, name='file_upload'),
    path('BP',views.blood_pressure, name="BP"),
    path('blood_sugar',views.blood_sugar, name= 'blood_sugar'),
    path('weight',views.weight,name="weight"),
    path('temperature',views.temperature,name='temperature'),
    path('pulse',views.pulse,name="pulse"),
    path('exercise',views.exercise,name="exercise"),
    path('sleep',views.sleep,name='sleep'),
    path('stress',views.stress,name='stress'),
    path('edit_bp',views.edit_bp, name='edit_bp'),
    path('edit_bp/<int:obj_id>',views.edit_bp, name='edit_bp_form'),
    path('edit_weight', views.edit_weight, name='edit_weight'),
    path('edit_weight/<int:obj_id>', views.edit_weight, name='edit_weight_form'),
    path('edit_sugar', views.edit_sugar, name='edit_sugar'),
    path('edit_sugar/<int:obj_id>', views.edit_sugar, name='edit_sugar_form'),
    path('edit_temperature', views.edit_temperature, name='edit_temperature'),
    path('edit_temperature/<int:obj_id>', views.edit_temperature, name='edit_temperature_form'),
    path('edit_pulse', views.edit_pulse, name='edit_pulse'),
    path('edit_pulse/<int:obj_id>', views.edit_pulse, name='edit_pulse_form'),
    path('edit_exercise', views.edit_exercise, name='edit_exercise'),
    path('edit_exercise/<int:obj_id>', views.edit_exercise, name='edit_exercise_form'),
    path('edit_sleep', views.edit_sleep, name='edit_sleep'),
    path('edit_sleep/<int:obj_id>', views.edit_sleep, name='edit_sleep_form'),
    path('edit_stress', views.edit_stress, name='edit_stress'),
    path('edit_stress/<int:obj_id>', views.edit_stress, name='edit_stress_form'),
    


]