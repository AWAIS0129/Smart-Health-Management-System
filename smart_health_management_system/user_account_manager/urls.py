from django.urls import path
from . import views

app_name = "user_accounts"
urlpatterns=[
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('set_profile', views.set_profile, name = 'set_profile'),
    path('profile_option/', views.profile_option, name='profile_option'),
    path('view_profile',views.view_profile,name = 'view_profile'),
    path('profile_edit',views.profile_edit, name='profile_edit'),
    
]