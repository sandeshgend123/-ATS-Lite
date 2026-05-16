from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Notifications
    - List notifications for current user
    - Mark as read/unread
    - Delete notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return notifications for current user only"""
        return Notification.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        """Delete notification"""
        if instance.user != self.request.user:
            return Response(
                {'error': 'You can only delete your own notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        if notification.user != request.user:
            return Response(
                {'error': 'You can only update your own notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Mark notification as unread"""
        notification = self.get_object()
        if notification.user != request.user:
            return Response(
                {'error': 'You can only update your own notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        notification.is_read = False
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get all unread notifications"""
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
