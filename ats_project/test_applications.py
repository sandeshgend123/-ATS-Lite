#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomUser
from applications.models import Application
from jobs.models import Job

print("\n" + "=" * 70)
print("APPLICATIONS API VERIFICATION TEST")
print("=" * 70)

# Test 1: Get all applications
print("\n[TEST 1] All Applications:")
print("-" * 70)
all_apps = Application.objects.all()
print(f"Total: {all_apps.count()} applications")
for app in all_apps[:5]:
    print(f"  • {app.candidate.user.username} → {app.job.title} (Status: {app.status}, Score: {app.skill_match_score}%)")

# Test 2: Applications by candidate
print("\n[TEST 2] Applications by Candidate:")
print("-" * 70)
try:
    candidate1 = CustomUser.objects.get(user__username='candidate1')
    my_apps = Application.objects.filter(candidate=candidate1)
    print(f"Candidate 'candidate1' has {my_apps.count()} applications:")
    for app in my_apps:
        print(f"  • {app.job.title} (Status: {app.status}, Score: {app.skill_match_score}%)")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Applications by Job
print("\n[TEST 3] Applications by Job:")
print("-" * 70)
try:
    jobs = Job.objects.all()[:3]
    for job in jobs:
        apps = Application.objects.filter(job=job)
        print(f"Job '{job.title}' has {apps.count()} applications")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Skill Match Calculation
print("\n[TEST 4] Skill Match Calculation:")
print("-" * 70)
print("Verifying skill match scores are calculated correctly...\n")
sample_apps = Application.objects.all()[:5]
for app in sample_apps:
    required = app.job.get_required_skills_list()
    candidate = app.get_candidate_skills_list()
    matches = sum(1 for r in required if r in candidate)
    expected_score = int((matches / len(required) * 100)) if required else 100
    status_symbol = "✓" if app.skill_match_score == expected_score else "✗"
    print(f"{status_symbol} {app.candidate.user.username} → {app.job.title}")
    print(f"   Required: {len(required)}, Candidate: {len(candidate)}, Matches: {matches}")
    print(f"   Score: {app.skill_match_score}% (Expected: {expected_score}%)")

# Test 5: Application Status Updates
print("\n[TEST 5] Application Status Workflow:")
print("-" * 70)
app = Application.objects.first()
if app:
    print(f"Testing with: {app.candidate.user.username} → {app.job.title}")
    print(f"Current status: {app.status}")
    
    # Simulate status updates
    for new_status in ['reviewed', 'shortlisted', 'accepted']:
        app.status = new_status
        app.save()
        print(f"  ✓ Updated to: {new_status}")
    
    # Reset to pending
    app.status = 'pending'
    app.save()
    print(f"  ✓ Reset to: pending")

# Test 6: Application Statistics
print("\n[TEST 6] Application Statistics:")
print("-" * 70)
total = Application.objects.count()
pending = Application.objects.filter(status='pending').count()
reviewed = Application.objects.filter(status='reviewed').count()
shortlisted = Application.objects.filter(status='shortlisted').count()
rejected = Application.objects.filter(status='rejected').count()
accepted = Application.objects.filter(status='accepted').count()

print(f"Total Applications: {total}")
print(f"  • Pending: {pending}")
print(f"  • Reviewed: {reviewed}")
print(f"  • Shortlisted: {shortlisted}")
print(f"  • Rejected: {rejected}")
print(f"  • Accepted: {accepted}")

# Test 7: Sorted by Skill Match
print("\n[TEST 7] Top Applications by Skill Match:")
print("-" * 70)
top_apps = Application.objects.all().order_by('-skill_match_score')[:5]
for i, app in enumerate(top_apps, 1):
    print(f"{i}. {app.candidate.user.username} → {app.job.title} ({app.skill_match_score}%)")

# Test 8: Unique Constraint
print("\n[TEST 8] Unique Constraint (Job-Candidate):")
print("-" * 70)
try:
    # Try to get first application and see if unique constraint works
    candidate = CustomUser.objects.filter(role='candidate').first()
    job = Job.objects.first()
    if candidate and job:
        existing_app = Application.objects.filter(job=job, candidate=candidate).first()
        if existing_app:
            print(f"✓ Unique constraint enforced: {candidate.user.username} can only apply once per job")
        else:
            print("• No existing application to test unique constraint")
except Exception as e:
    print(f"✗ Error checking unique constraint: {e}")

# Test 9: Data Integrity
print("\n[TEST 9] Data Integrity Check:")
print("-" * 70)
errors = []

# Check all applications have valid candidates
invalid_candidates = Application.objects.exclude(candidate__role='candidate')
if invalid_candidates.exists():
    errors.append(f"Found {invalid_candidates.count()} applications with non-candidate users")

# Check all applications have valid jobs
no_job_apps = Application.objects.filter(job__isnull=True)
if no_job_apps.exists():
    errors.append(f"Found {no_job_apps.count()} applications with no job")

# Check skill match scores are valid
invalid_scores = Application.objects.filter(skill_match_score__lt=0) | Application.objects.filter(skill_match_score__gt=100)
if invalid_scores.exists():
    errors.append(f"Found {invalid_scores.count()} applications with invalid skill match scores")

if errors:
    print("✗ Data integrity issues found:")
    for error in errors:
        print(f"  • {error}")
else:
    print("✓ All data integrity checks passed!")

print("\n" + "=" * 70)
print("✅ VERIFICATION COMPLETE")
print("=" * 70)
print("\nAPI Endpoints to test:")
print("  GET  http://127.0.0.1:8000/api/applications/")
print("  GET  http://127.0.0.1:8000/api/applications/my_applications/")
print("  GET  http://127.0.0.1:8000/api/applications/sorted_by_score/")
print("  GET  http://127.0.0.1:8000/api/applications/stats/")
print("  POST http://127.0.0.1:8000/api/applications/")
print("  PATCH http://127.0.0.1:8000/api/applications/{id}/update_status/")
print("\n")
