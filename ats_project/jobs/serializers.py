from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.user.get_full_name', read_only=True)
    required_skills_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'required_skills', 'required_skills_list',
            'company', 'company_name', 'location', 'salary_min', 'salary_max',
            'experience_level', 'job_type', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_required_skills_list(self, obj):
        return obj.get_required_skills_list()
