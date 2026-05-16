from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count
from .models import Application
from .serializers import ApplicationSerializer, ApplicationStatsSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Job Applications
    - Create application (candidate only)
    - List applications for a job (employer)
    - List my applications (candidate)
    - Update application status (employer)
    - Calculate skill match score
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['candidate__user__first_name', 'candidate__user__last_name', 'candidate__user__email']
    ordering_fields = ['skill_match_score', 'applied_at', 'status']
    ordering = ['-skill_match_score', '-applied_at']
    
    def get_queryset(self):
        """Filter applications based on user role"""
        user = self.request.user
        try:
            from accounts.models import CustomUser
            custom_user = CustomUser.objects.get(user=user)
            
            if self.action == 'my_applications':
                # Candidates see their own applications
                return Application.objects.filter(candidate=custom_user)
            elif self.action == 'job_applications':
                # Employers see applications for their jobs
                return Application.objects.filter(job__company=custom_user)
            else:
                # By default, show all (filtered by permissions in methods)
                return super().get_queryset()
        except:
            return Application.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Create application with proper error handling"""
        try:
            from accounts.models import CustomUser
            candidate = CustomUser.objects.get(user=request.user)
            
            if candidate.role != 'candidate':
                return Response(
                    {'error': 'Only candidates can apply for jobs'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        """Create application and calculate skill match"""
        from accounts.models import CustomUser
        from notifications.models import Notification
        from .utils import generate_application_excel
        
        candidate = CustomUser.objects.get(user=self.request.user)
        application = serializer.save(candidate=candidate)
        
        # Calculate skill match score
        application.skill_match_score = application.calculate_skill_match_score()
        application.save()
        
        # Generate Excel file with application details
        excel_file = generate_application_excel(application)
        application.application_excel.save(excel_file.name, excel_file, save=True)
        
        # Create notification
        job = application.job
        Notification.objects.create(
            user=job.company.user,
            title=f'New Application for {job.title}',
            message=f'{candidate.user.get_full_name() or candidate.user.username} applied for {job.title}',
            notification_type='application',
            related_application=application
        )
    
    def perform_update(self, serializer):
        """Update application status"""
        application = self.get_object()
        try:
            from accounts.models import CustomUser
            employer = CustomUser.objects.get(user=self.request.user)
            if application.job.company != employer:
                return Response(
                    {'error': 'You can only update applications for your jobs'},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save()
        except:
            pass
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Get applications submitted by current candidate"""
        applications = self.get_queryset()
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='job/(?P<job_id>[^/.]+)')
    def job_applications(self, request, job_id=None):
        """Get all applications for a specific job"""
        try:
            from jobs.models import Job
            from accounts.models import CustomUser
            
            job = Job.objects.get(id=job_id)
            employer = CustomUser.objects.get(user=request.user)
            
            if job.company != employer:
                return Response(
                    {'error': 'You can only view applications for your jobs'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            applications = Application.objects.filter(job=job).order_by('-skill_match_score')
            serializer = self.get_serializer(applications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get application statistics"""
        try:
            from accounts.models import CustomUser
            custom_user = CustomUser.objects.get(user=request.user)
            
            if custom_user.role == 'employer':
                # Employer stats
                applications = Application.objects.filter(job__company=custom_user)
            else:
                # Candidate stats
                applications = Application.objects.filter(candidate=custom_user)
            
            stats = {
                'total_applications': applications.count(),
                'pending_count': applications.filter(status='pending').count(),
                'reviewed_count': applications.filter(status='reviewed').count(),
                'shortlisted_count': applications.filter(status='shortlisted').count(),
                'rejected_count': applications.filter(status='rejected').count(),
                'accepted_count': applications.filter(status='accepted').count(),
            }
            
            serializer = ApplicationStatsSerializer(stats)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status"""
        application = self.get_object()
        status_value = request.data.get('status')
        
        if status_value not in dict(Application.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from accounts.models import CustomUser
            employer = CustomUser.objects.get(user=request.user)
            if application.job.company != employer:
                return Response(
                    {'error': 'You can only update applications for your jobs'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            application.status = status_value
            application.save()
            
            # Create notification for candidate
            from notifications.models import Notification
            Notification.objects.create(
                user=application.candidate.user,
                title=f'Application Status Update',
                message=f'Your application for {application.job.title} has been {status_value}',
                notification_type='status_update',
                related_application=application
            )
            
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def sorted_by_score(self, request):
        """Get all applications sorted by skill match score"""
        job_id = request.query_params.get('job_id')
        
        try:
            if job_id:
                from jobs.models import Job
                from accounts.models import CustomUser
                
                job = Job.objects.get(id=job_id)
                employer = CustomUser.objects.get(user=request.user)
                
                if job.company != employer:
                    return Response(
                        {'error': 'You can only view applications for your jobs'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                applications = Application.objects.filter(job=job).order_by('-skill_match_score')
            else:
                # Employer gets all applications for their jobs
                from accounts.models import CustomUser
                employer = CustomUser.objects.get(user=request.user)
                applications = Application.objects.filter(job__company=employer).order_by('-skill_match_score')
            
            serializer = self.get_serializer(applications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
