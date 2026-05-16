from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
from accounts.models import CustomUser


class Application(models.Model):
    """Job application from candidate"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications', limit_choices_to={'role': 'candidate'})
    candidate_skills = models.CharField(max_length=500, help_text="Skills separated by commas")
    cover_letter = models.TextField(blank=True, null=True)
    skill_match_score = models.IntegerField(default=0, help_text="Skill match percentage (0-100)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Upload PDF resume")
    application_excel = models.FileField(upload_to='applications/excel/', blank=True, null=True, help_text="Application details Excel file")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'candidate']
        indexes = [
            models.Index(fields=['job', 'candidate']),
            models.Index(fields=['status']),
            models.Index(fields=['-skill_match_score']),
        ]
    
    def get_candidate_skills_list(self):
        """Return candidate skills as a list"""
        return [skill.strip().lower() for skill in self.candidate_skills.split(',')]
    
    def calculate_skill_match_score(self):
        """
        Calculate skill match percentage based on:
        - Required skills vs candidate skills
        - Matching ratio
        """
        required_skills = self.job.get_required_skills_list()
        candidate_skills = self.get_candidate_skills_list()
        
        if not required_skills:
            return 100
        
        matches = 0
        for skill in required_skills:
            if skill in candidate_skills:
                matches += 1
        
        score = (matches / len(required_skills)) * 100
        return int(round(score))
