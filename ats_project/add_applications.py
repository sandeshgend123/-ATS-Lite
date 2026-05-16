#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomUser
from jobs.models import Job
from applications.models import Application

print("=" * 60)
print("CREATING TEST DATA FOR APPLICATIONS")
print("=" * 60)

# Create test candidates
candidate_data = [
    {'username': 'candidate1', 'email': 'candidate1@test.com', 'name': 'John', 'skills': 'python, django, rest_api, postgresql'},
    {'username': 'candidate2', 'email': 'candidate2@test.com', 'name': 'Jane', 'skills': 'javascript, react, typescript, css'},
    {'username': 'candidate3', 'email': 'candidate3@test.com', 'name': 'Bob', 'skills': 'python, django, aws, docker'},
]

candidates = []
print("\nCreating test candidates...")
for data in candidate_data:
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={'email': data['email'], 'first_name': data['name']}
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"✓ Created user: {data['username']}")
    
    custom_user, created = CustomUser.objects.get_or_create(
        user=user,
        defaults={'role': 'candidate', 'phone': '9876543210'}
    )
    if created:
        print(f"✓ Created candidate profile: {data['username']}")
    candidates.append((custom_user, data['skills']))

# Get the first job or create one
print("\nFetching jobs...")
jobs = Job.objects.all()[:5]
print(f"Found {jobs.count()} jobs")

# Create applications
print("\nCreating applications...")
application_count = 0
for i, (candidate, skills) in enumerate(candidates):
    for job in jobs[:3]:  # Apply to first 3 jobs
        app, created = Application.objects.get_or_create(
            job=job,
            candidate=candidate,
            defaults={
                'candidate_skills': skills,
                'cover_letter': f'I am interested in the {job.title} position. I have experience with {skills}.',
            }
        )
        if created:
            # Calculate skill match
            app.skill_match_score = app.calculate_skill_match_score()
            app.save()
            print(f"✓ {candidate.user.username} applied for {job.title} (Score: {app.skill_match_score}%)")
            application_count += 1
        else:
            print(f"• {candidate.user.username} already applied for {job.title}")

print("\n" + "=" * 60)
print("APPLICATIONS SUMMARY")
print("=" * 60)

# Show all applications
all_apps = Application.objects.all().select_related('job', 'candidate')
print(f"\nTotal Applications: {all_apps.count()}")

print("\nApplications by Status:")
for status, label in Application.STATUS_CHOICES:
    count = all_apps.filter(status=status).count()
    print(f"  {label}: {count}")

print("\nTop Applications by Skill Match:")
top_apps = all_apps.order_by('-skill_match_score')[:10]
for app in top_apps:
    print(f"  • {app.candidate.user.username} → {app.job.title} ({app.skill_match_score}%)")

print("\n✅ Test data created successfully!")
print("\nAccess Applications API at:")
print("  • http://127.0.0.1:8000/api/applications/")
print("  • http://127.0.0.1:8000/api/applications/my_applications/")
print("  • http://127.0.0.1:8000/api/applications/sorted_by_score/")
print("  • http://127.0.0.1:8000/api/applications/stats/")
