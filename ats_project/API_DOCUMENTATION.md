# API Documentation

## ATS Lite - Job Application System API

**Base URL:** `http://localhost:8000/api/`

---

## Authentication

### Login
```
POST /api/accounts/register/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_pass123",
    "password2": "secure_pass123",
    "role": "candidate" // or "employer"
}
```

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/register/register/` | Register new user |
| GET | `/accounts/users/me/` | Get current user |
| GET | `/accounts/profiles/me/` | Get current user profile |
| GET | `/jobs/` | List all active jobs |
| POST | `/jobs/` | Create new job (employer) |
| GET | `/jobs/my_jobs/` | Get my jobs (employer) |
| POST | `/jobs/{id}/close_job/` | Close job (employer) |
| GET | `/applications/` | List applications |
| POST | `/applications/` | Apply for job (candidate) |
| GET | `/applications/my_applications/` | Get my applications (candidate) |
| GET | `/applications/job/{job_id}/` | Get job applications (employer) |
| GET | `/applications/sorted_by_score/` | Get applications sorted by score |
| POST | `/applications/{id}/update_status/` | Update application status |
| GET | `/applications/stats/` | Get statistics |
| GET | `/notifications/` | List notifications |
| GET | `/notifications/unread/` | Get unread notifications |
| GET | `/notifications/unread_count/` | Get unread count |
| POST | `/notifications/{id}/mark_as_read/` | Mark notification as read |
| DELETE | `/notifications/{id}/` | Delete notification |

---

## Complete Request/Response Examples

### 1. User Registration

**Request:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "candidate",
    "phone": "555-1234"
  }'
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully"
}
```

---

### 2. Post a Job

**Request:**
```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer with 5+ years of experience",
    "required_skills": "python,django,postgresql,rest,docker",
    "location": "San Francisco, CA",
    "salary_min": "120000",
    "salary_max": "180000",
    "experience_level": "senior",
    "job_type": "full-time"
  }'
```

**Response (201 Created):**
```json
{
    "id": 1,
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer with 5+ years of experience",
    "required_skills": "python,django,postgresql,rest,docker",
    "required_skills_list": ["python", "django", "postgresql", "rest", "docker"],
    "company": 1,
    "company_name": "Tech Corp",
    "location": "San Francisco, CA",
    "salary_min": "120000.00",
    "salary_max": "180000.00",
    "experience_level": "senior",
    "job_type": "full-time",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
}
```

---

### 3. Apply for a Job

**Request:**
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "job": 1,
    "candidate_skills": "python,django,postgresql,rest,docker,kubernetes",
    "cover_letter": "I am very interested in this position. I have 6 years of Python experience and have worked with Django extensively."
  }'
```

**Response (201 Created):**
```json
{
    "id": 1,
    "job": 1,
    "job_title": "Senior Python Developer",
    "candidate": 2,
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "candidate_skills": "python,django,postgresql,rest,docker,kubernetes",
    "candidate_skills_list": ["python", "django", "postgresql", "rest", "docker", "kubernetes"],
    "required_skills": ["python", "django", "postgresql", "rest", "docker"],
    "cover_letter": "I am very interested in this position...",
    "skill_match_score": 100,
    "status": "pending",
    "resume_url": null,
    "applied_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### 4. Get Candidates Sorted by Score

**Request:**
```bash
curl -X GET "http://localhost:8000/api/applications/sorted_by_score/?job_id=1" \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "job": 1,
        "job_title": "Senior Python Developer",
        "candidate": 2,
        "candidate_name": "John Doe",
        "candidate_email": "john@example.com",
        "skill_match_score": 100,
        "status": "pending",
        "applied_at": "2024-01-15T10:30:00Z"
    },
    {
        "id": 2,
        "job": 1,
        "job_title": "Senior Python Developer",
        "candidate": 3,
        "candidate_name": "Jane Smith",
        "candidate_email": "jane@example.com",
        "skill_match_score": 80,
        "status": "pending",
        "applied_at": "2024-01-14T09:15:00Z"
    },
    {
        "id": 3,
        "job": 1,
        "job_title": "Senior Python Developer",
        "candidate": 4,
        "candidate_name": "Bob Johnson",
        "candidate_email": "bob@example.com",
        "skill_match_score": 60,
        "status": "pending",
        "applied_at": "2024-01-13T14:45:00Z"
    }
]
```

---

### 5. Update Application Status

**Request:**
```bash
curl -X POST http://localhost:8000/api/applications/1/update_status/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "status": "shortlisted"
  }'
```

**Response (200 OK):**
```json
{
    "id": 1,
    "job": 1,
    "job_title": "Senior Python Developer",
    "candidate": 2,
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "candidate_skills": "python,django,postgresql,rest,docker,kubernetes",
    "cover_letter": "I am very interested...",
    "skill_match_score": 100,
    "status": "shortlisted",
    "applied_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### 6. Get Notifications

**Request:**
```bash
curl -X GET "http://localhost:8000/api/notifications/" \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "New Application for Senior Python Developer",
            "message": "John Doe applied for Senior Python Developer",
            "notification_type": "application",
            "is_read": false,
            "application_id": 1,
            "job_title": "Senior Python Developer",
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "title": "Application Status Update",
            "message": "Your application for Senior Python Developer has been shortlisted",
            "notification_type": "status_update",
            "is_read": false,
            "application_id": 1,
            "job_title": "Senior Python Developer",
            "created_at": "2024-01-15T11:00:00Z"
        }
    ]
}
```

---

### 7. Mark Notification as Read

**Request:**
```bash
curl -X POST http://localhost:8000/api/notifications/1/mark_as_read/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "New Application for Senior Python Developer",
    "message": "John Doe applied for Senior Python Developer",
    "notification_type": "application",
    "is_read": true,
    "application_id": 1,
    "job_title": "Senior Python Developer",
    "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 8. Get Unread Notifications Count

**Request:**
```bash
curl -X GET "http://localhost:8000/api/notifications/unread_count/" \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
    "unread_count": 2
}
```

---

### 9. Get Application Statistics

**Request:**
```bash
curl -X GET "http://localhost:8000/api/applications/stats/" \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response (200 OK) - Employer:**
```json
{
    "total_applications": 15,
    "pending_count": 5,
    "reviewed_count": 3,
    "shortlisted_count": 4,
    "rejected_count": 2,
    "accepted_count": 1
}
```

**Response (200 OK) - Candidate:**
```json
{
    "total_applications": 3,
    "pending_count": 1,
    "reviewed_count": 1,
    "shortlisted_count": 1,
    "rejected_count": 0,
    "accepted_count": 0
}
```

---

## Filtering and Search

### Search Jobs
```bash
curl -X GET "http://localhost:8000/api/jobs/?search=python&experience_level=senior" \
  -H "Authorization: Token YOUR_TOKEN"
```

### Filter Applications by Score
```bash
curl -X GET "http://localhost:8000/api/applications/?skill_match_score__gte=75" \
  -H "Authorization: Token YOUR_TOKEN"
```

### Pagination
```bash
curl -X GET "http://localhost:8000/api/jobs/?page=2" \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid status"
}
```

### 403 Forbidden
```json
{
    "error": "You can only view applications for your jobs"
}
```

### 404 Not Found
```json
{
    "error": "Not found"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Resource deleted |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Server Error |

---

## Rate Limiting

No rate limiting is applied in this version.

---

## CORS

CORS is enabled for localhost. For production, configure in settings.py:

```python
CORS_ALLOWED_ORIGINS = [
    "http://yourdomain.com",
]
```

---

## Pagination

Default page size: **10 items per page**

Change in `settings.py`:
```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 10
}
```

---

## Skill Matching Algorithm

Score = (Matched Skills / Total Required Skills) × 100

**Example:**
- Job requires: `python, django, postgresql, rest`
- Candidate has: `python, django, postgresql, docker`
- Matched: 3 out of 4
- Score: (3/4) × 100 = **75%**

---

**Last Updated:** 2024-01-15
