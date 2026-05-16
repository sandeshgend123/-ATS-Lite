from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser

class Job(models.Model):
    """Job posting model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.CharField(max_length=500, help_text="Skills separated by commas")
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs', limit_choices_to={'role': 'employer'})
    location = models.CharField(max_length=255)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
        ],
        default='entry'
    )
    job_type = models.CharField(
        max_length=20,
        choices=[
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('remote', 'Remote'),
        ],
        default='full-time'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.company.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['is_active']),
        ]
    
    def get_required_skills_list(self):
        """Return required skills as a list"""
        return [skill.strip().lower() for skill in self.required_skills.split(',')]
