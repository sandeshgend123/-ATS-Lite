from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'job_type', 'experience_level', 'created_at']
    search_fields = ['title', 'description', 'location', 'required_skills']
    readonly_fields = ['created_at', 'updated_at']
