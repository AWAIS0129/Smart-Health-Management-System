"""
URL configuration for smart_health_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_account_manager.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('data/', include('health_data_manager.urls')),
    path("visualization/", include('data_visualization.urls')),
    path("report_engine/", include('report_engine.urls')),
    path("notifications/",include('notifications.urls')),
    path('ai_engine/', include('ai_engine.urls')),
]
