from .models import UserNotification
from django.utils import timezone

class NotificationService:
  
    @staticmethod
    def create_notification(user, title, message, priority = None, channel = None, expires_in_days = None):
      
        
        priorities = UserNotification.Priority.values
        
        
        if priority  not in priorities:
            
            priority = UserNotification.Priority.LOW
            
        if channel is None:
            
            channel = UserNotification.Channel.IN_APP
            
        if expires_in_days is None:
            
            expires_in_days = 3
            
        expiry_date = timezone.now() + timezone.timedelta(days=expires_in_days)
            
        notification = UserNotification.objects.create(
            user = user,
            title = title,
            message = message,
            priority = priority,
            channel = channel,
            expires_at = expiry_date,
        
            
        )
        return notification
    
    
    @staticmethod
    def mark_as_read(user, notification_id):
        record = UserNotification.objects.filter(
            user=user,
            id=notification_id
        )
        record.update(is_read = True)
        
    @staticmethod
    def get_unread_notifications(user):
        return UserNotification.objects.filter(
            user = user,
            is_read = False
        )
    
    @staticmethod
    def get_all_notifications(user):
        return UserNotification.objects.filter(
            user = user,
            
            
        )
    @staticmethod
    def get_all_active_notifications(user):
        notifications = NotificationService.get_all_notifications(user).exclude( expires_at__lt=timezone.now())
        return notifications
    
    @staticmethod
    def get_notification(user,notification_id):
        return UserNotification.objects.filter(
            user = user,
            id = notification_id
        ).first()
            
        
        
    