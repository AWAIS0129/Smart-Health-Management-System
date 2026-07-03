from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services import NotificationService


# Create your views here.

def home(request):
    
    context = {
        'data':list( NotificationService.get_all_active_notifications(request.user)),
        }
    return render(request, 'notifications/home.html',context)

def mark_as_read(request, notification_id):
    NotificationService.mark_as_read(request.user,notification_id)
    notification = NotificationService.get_notification(request.user,notification_id)
    context = {
        'notification':notification
    }
    return render(request,'notifications/notification_card.html', context)





    