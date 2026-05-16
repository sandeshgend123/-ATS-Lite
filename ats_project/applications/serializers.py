from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.user.get_full_name', read_only=True)
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    required_skills = serializers.SerializerMethodField()
    candidate_skills_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name', 'candidate_email',
            'candidate_skills', 'candidate_skills_list', 'required_skills',
            'cover_letter', 'skill_match_score', 'status', 'resume', 'application_excel',
            'applied_at', 'updated_at'
        ]
        read_only_fields = ['id', 'candidate', 'candidate_name', 'candidate_email', 'skill_match_score', 'application_excel', 'applied_at', 'updated_at']
    
    def get_required_skills(self, obj):
        return obj.job.get_required_skills_list()
    
    def get_candidate_skills_list(self, obj):
        return obj.get_candidate_skills_list()


class ApplicationStatsSerializer(serializers.Serializer):
    """Serializer for application statistics"""
    total_applications = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    reviewed_count = serializers.IntegerField()
    shortlisted_count = serializers.IntegerField()
    rejected_count = serializers.IntegerField()
    accepted_count = serializers.IntegerField()
