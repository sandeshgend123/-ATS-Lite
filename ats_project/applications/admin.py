from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'skill_match_score', 'status', 'applied_at']
    list_filter = ['status', 'skill_match_score', 'applied_at']
    search_fields = ['candidate__user__username', 'job__title']
    readonly_fields = ['skill_match_score', 'applied_at', 'updated_at']
