from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(models.Model):
    """Extended user model with additional fields"""
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"
    
    class Meta:
        ordering = ['-created_at']
