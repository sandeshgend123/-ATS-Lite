#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomUser
from jobs.models import Job

# Get or create a test employer user
employer_user, created = User.objects.get_or_create(
    username='employer1',
    defaults={'email': 'employer@test.com', 'first_name': 'Tech', 'last_name': 'Company'}
)
if created:
    employer_user.set_password('password123')
    employer_user.save()
    print("✓ Created employer user")
else:
    print("• Employer user already exists")

# Create CustomUser for employer if doesn't exist
employer_profile, created = CustomUser.objects.get_or_create(
    user=employer_user,
    defaults={'role': 'employer', 'company_name': 'Tech Corp', 'phone': '1234567890'}
)
if created:
    print("✓ Created employer profile")

# Create 10 sample jobs
jobs_data = [
    {'title': 'Senior Python Developer', 'description': 'Looking for an experienced Python developer with Django expertise', 'required_skills': 'python, django, rest_api, postgresql', 'location': 'New York, NY', 'salary_min': 120000, 'salary_max': 160000, 'experience_level': 'senior', 'job_type': 'full-time'},
    {'title': 'Frontend React Developer', 'description': 'Build responsive UIs with React and TypeScript', 'required_skills': 'javascript, react, typescript, css', 'location': 'San Francisco, CA', 'salary_min': 110000, 'salary_max': 150000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'DevOps Engineer', 'description': 'Manage cloud infrastructure and CI/CD pipelines', 'required_skills': 'docker, kubernetes, aws, ci-cd', 'location': 'Seattle, WA', 'salary_min': 130000, 'salary_max': 170000, 'experience_level': 'senior', 'job_type': 'full-time'},
    {'title': 'Junior Web Developer', 'description': 'Get started with modern web development', 'required_skills': 'html, css, javascript, git', 'location': 'Remote', 'salary_min': 60000, 'salary_max': 80000, 'experience_level': 'junior', 'job_type': 'full-time'},
    {'title': 'Data Scientist', 'description': 'Analyze data and build machine learning models', 'required_skills': 'python, pandas, scikit-learn, sql', 'location': 'Boston, MA', 'salary_min': 125000, 'salary_max': 165000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'Full Stack Developer', 'description': 'Work on both frontend and backend systems', 'required_skills': 'javascript, react, node.js, postgresql', 'location': 'Austin, TX', 'salary_min': 100000, 'salary_max': 140000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'Mobile App Developer', 'description': 'Develop iOS and Android applications', 'required_skills': 'swift, kotlin, react-native, mobile', 'location': 'Los Angeles, CA', 'salary_min': 105000, 'salary_max': 145000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'Database Administrator', 'description': 'Manage and optimize databases', 'required_skills': 'postgresql, mysql, sql, database-administration', 'location': 'Chicago, IL', 'salary_min': 95000, 'salary_max': 130000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'QA Engineer', 'description': 'Test software and ensure quality', 'required_skills': 'testing, selenium, qa, automation', 'location': 'Denver, CO', 'salary_min': 80000, 'salary_max': 110000, 'experience_level': 'mid', 'job_type': 'full-time'},
    {'title': 'Solutions Architect', 'description': 'Design technical solutions for clients', 'required_skills': 'architecture, design-patterns, aws, cloud', 'location': 'New York, NY', 'salary_min': 140000, 'salary_max': 180000, 'experience_level': 'senior', 'job_type': 'full-time'},
]

print("\nAdding 10 jobs...")
for job_data in jobs_data:
    job, created = Job.objects.get_or_create(
        title=job_data['title'],
        company=employer_profile,
        defaults={
            'description': job_data['description'],
            'required_skills': job_data['required_skills'],
            'location': job_data['location'],
            'salary_min': job_data['salary_min'],
            'salary_max': job_data['salary_max'],
            'experience_level': job_data['experience_level'],
            'job_type': job_data['job_type'],
            'is_active': True
        }
    )
    if created:
        print(f"✓ Created: {job.title}")
    else:
        print(f"• Already exists: {job.title}")

print(f"\n✅ Total jobs in database: {Job.objects.count()}")
