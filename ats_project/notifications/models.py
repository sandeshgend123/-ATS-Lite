from django.db import models
from django.contrib.auth.models import User
from applications.models import Application


class Notification(models.Model):
    """Notification model for users"""
    NOTIFICATION_TYPES = [
        ('application', 'New Application'),
        ('status_update', 'Application Status Update'),
        ('job_closed', 'Job Closed'),
        ('job_reminder', 'Job Reminder'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='other')
    is_read = models.BooleanField(default=False)
    related_application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
