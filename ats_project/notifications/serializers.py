from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    application_id = serializers.IntegerField(source='related_application.id', read_only=True, allow_null=True)
    job_title = serializers.CharField(source='related_application.job.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'is_read',
            'application_id', 'job_title', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
