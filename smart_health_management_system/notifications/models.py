from django.db import models
from user_account_manager.models import User

# Create your models here.

class UserNotification(models.Model):

    
    
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Informational'
        MEDIUM = 'MEDIUM', 'Normal'
        HIGH = 'HIGH', 'Important'
        CRITICAL = 'CRITICAL', 'Warning'
        
    class Channel(models.TextChoices):
        IN_APP = 'APP', 'Notification_page'
        EMAIL = 'EMAIL', 'Email'
        ALL_CHANNEL = 'ALL', 'All_channels'
        
        
    # Basic fields related to a notification
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=100)
    message = models.TextField()
    
    
    # notification type fields
        
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    
    # status fields
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['priority' ,'-created_at'])
        ]
        ordering = [
            '-priority',
            '-created_at'
        ]
    
    def __str__(self):
        return f"[{self.priority}] {self.title} for {self.user}"
    
    def is_alert(self):
        return self.priority in [self.Priority.HIGH, self.Priority.CRITICAL]
        
        
    