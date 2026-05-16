from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Job postings
    - List all active jobs
    - Create job (employer only)
    - Update job (employer only)
    - Delete job (employer only)
    """
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'location', 'required_skills']
    ordering_fields = ['created_at', 'salary_max', 'salary_min']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter jobs based on user"""
        if self.action == 'my_jobs':
            return Job.objects.filter(company__user=self.request.user)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        """Set company to current user's CustomUser"""
        try:
            from accounts.models import CustomUser
            company = CustomUser.objects.get(user=self.request.user)
            if company.role != 'employer':
                return Response(
                    {'error': 'Only employers can create jobs'},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save(company=company)
        except:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_update(self, serializer):
        """Ensure only job owner can update"""
        job = self.get_object()
        from accounts.models import CustomUser
        company = CustomUser.objects.get(user=self.request.user)
        if job.company != company:
            return Response(
                {'error': 'You can only update your own jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure only job owner can delete"""
        from accounts.models import CustomUser
        company = CustomUser.objects.get(user=self.request.user)
        if instance.company != company:
            return Response(
                {'error': 'You can only delete your own jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        """Get jobs posted by current user"""
        jobs = self.get_queryset()
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close_job(self, request, pk=None):
        """Close a job posting"""
        job = self.get_object()
        from accounts.models import CustomUser
        company = CustomUser.objects.get(user=request.user)
        if job.company != company:
            return Response(
                {'error': 'You can only close your own jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        job.is_active = False
        job.save()
        return Response({'status': 'Job closed successfully'})
