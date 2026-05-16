from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from project root
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from views import (
    index, login_view, register_view, logout_view,
    jobs_list, job_create, job_detail, candidates_list, notifications_view, profile_view,
    admin_applications_view
)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    
    # Auth URLs
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Frontend URLs
    path('jobs/', jobs_list, name='jobs'),
    path('jobs/create/', job_create, name='job_create'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('candidates/', candidates_list, name='candidates'),
    path('notifications/', notifications_view, name='notifications'),
    path('profile/', profile_view, name='profile'),
    path('admin-applications/', admin_applications_view, name='admin_applications'),
    
    # API URLs
    path('api/jobs/', include('jobs.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
