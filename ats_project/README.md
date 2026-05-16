# ATS Lite - Job Application System

A complete Applicant Tracking System (ATS) built with Django, Python, and SQL. This is a production-ready system for managing job postings, candidate applications, skill matching, and notifications.

## 🎯 Features

### Core Features
✅ **Job Management**
- Post jobs with required skills
- Search and filter jobs
- Job status management
- Multiple job types (Full-time, Part-time, Contract, Remote)

✅ **Candidate Applications**
- Apply for jobs with skills and cover letter
- Automatic skill matching algorithm
- Application status tracking (Pending, Reviewed, Shortlisted, Accepted, Rejected)
- Score calculation based on skill match

✅ **Skill Matching Algorithm**
- Calculates match percentage automatically
- Compares candidate skills with job requirements
- Instant scoring for better decision making

✅ **Notifications**
- Real-time notifications for new applications
- Application status updates
- Mark as read/unread
- Email-style notification system

✅ **User Roles**
- Employer: Post jobs and manage applications
- Candidate: Apply for jobs and track applications

✅ **Filtering & Pagination**
- Search jobs and candidates
- Filter by score, experience level, job type
- Paginated results (10 items per page)
- Responsive table views

### Bonus Features
✅ REST APIs with full documentation
✅ Admin dashboard for management
✅ Responsive Bootstrap UI
✅ Easy PythonAnywhere deployment

## 📋 Prerequisites

- Python 3.8+
- pip
- Git (for version control)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ats_project
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
Follow prompts to create admin account.

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
- Use session-based authentication
- Login via `/login/` page or API

### Endpoints

#### **Accounts API** (`/api/accounts/`)

**Register**
```
POST /api/accounts/register/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_pass123",
    "password2": "secure_pass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "candidate",  // or "employer"
    "phone": "1234567890",
    "company_name": "Acme Corp"  // only if employer
}

Response: 201 Created
{
    "message": "User registered successfully"
}
```

**Get Current User Profile**
```
GET /api/accounts/profiles/me/

Response: 200 OK
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "role": "candidate",
    "phone": "1234567890",
    "company_name": null,
    "bio": "Software developer",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
}
```

#### **Jobs API** (`/api/jobs/`)

**List All Jobs**
```
GET /api/jobs/?search=python&experience_level=mid

Response: 200 OK
{
    "count": 15,
    "next": "http://localhost:8000/api/jobs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Senior Python Developer",
            "description": "Looking for experienced Python developer...",
            "required_skills": "python, django, sql, rest",
            "required_skills_list": ["python", "django", "sql", "rest"],
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
    ]
}
```

**Create Job (Employer Only)**
```
POST /api/jobs/

Headers:
Authorization: Bearer <token>

{
    "title": "Full Stack Developer",
    "description": "We are looking for a Full Stack Developer...",
    "required_skills": "javascript, react, nodejs, mongodb",
    "location": "New York, NY",
    "salary_min": "100000",
    "salary_max": "150000",
    "experience_level": "mid",
    "job_type": "full-time"
}

Response: 201 Created
{
    "id": 1,
    "title": "Full Stack Developer",
    ...
}
```

**Get My Jobs (Employer)**
```
GET /api/jobs/my_jobs/

Response: 200 OK
[
    { ... job objects ... }
]
```

**Close Job**
```
POST /api/jobs/{id}/close_job/

Response: 200 OK
{
    "status": "Job closed successfully"
}
```

#### **Applications API** (`/api/applications/`)

**Apply for Job (Candidate)**
```
POST /api/applications/

Headers:
Authorization: Bearer <token>

{
    "job": 1,
    "candidate_skills": "javascript, react, nodejs, html, css",
    "cover_letter": "I am very interested in this position...",
    "resume_url": "https://example.com/resume.pdf"
}

Response: 201 Created
{
    "id": 1,
    "job": 1,
    "job_title": "Full Stack Developer",
    "candidate": 1,
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "candidate_skills": "javascript, react, nodejs, html, css",
    "candidate_skills_list": ["javascript", "react", "nodejs", "html", "css"],
    "required_skills": ["javascript", "react", "nodejs", "mongodb"],
    "cover_letter": "I am very interested...",
    "skill_match_score": 75,
    "status": "pending",
    "resume_url": "https://example.com/resume.pdf",
    "applied_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**Get My Applications (Candidate)**
```
GET /api/applications/my_applications/

Response: 200 OK
{
    "count": 5,
    "results": [ ... applications ... ]
}
```

**Get Job Applications (Employer)**
```
GET /api/applications/job/{job_id}/

Response: 200 OK
[
    {
        "id": 1,
        "job": 1,
        "candidate": 1,
        "candidate_name": "John Doe",
        "skill_match_score": 85,
        "status": "pending",
        ...
    }
]
```

**Get Applications Sorted by Score**
```
GET /api/applications/sorted_by_score/?job_id=1

Response: 200 OK
[
    { "skill_match_score": 95, ... },
    { "skill_match_score": 85, ... },
    { "skill_match_score": 70, ... }
]
```

**Update Application Status (Employer)**
```
POST /api/applications/{id}/update_status/

{
    "status": "shortlisted"  // or "reviewed", "accepted", "rejected"
}

Response: 200 OK
{ ... updated application ... }
```

**Get Application Statistics**
```
GET /api/applications/stats/

Response: 200 OK
{
    "total_applications": 10,
    "pending_count": 3,
    "reviewed_count": 2,
    "shortlisted_count": 3,
    "rejected_count": 1,
    "accepted_count": 1
}
```

#### **Notifications API** (`/api/notifications/`)

**List Notifications**
```
GET /api/notifications/

Response: 200 OK
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "title": "New Application for Senior Python Developer",
            "message": "John Doe applied for Senior Python Developer",
            "notification_type": "application",
            "is_read": false,
            "application_id": 1,
            "job_title": "Senior Python Developer",
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

**Get Unread Notifications**
```
GET /api/notifications/unread/

Response: 200 OK
[ ... unread notifications ... ]
```

**Get Unread Count**
```
GET /api/notifications/unread_count/

Response: 200 OK
{
    "unread_count": 3
}
```

**Mark as Read**
```
POST /api/notifications/{id}/mark_as_read/

Response: 200 OK
{ ... notification with is_read: true ... }
```

**Mark as Unread**
```
POST /api/notifications/{id}/mark_as_unread/

Response: 200 OK
{ ... notification with is_read: false ... }
```

**Mark All as Read**
```
POST /api/notifications/mark_all_as_read/

Response: 200 OK
{
    "status": "All notifications marked as read"
}
```

**Delete Notification**
```
DELETE /api/notifications/{id}/

Response: 204 No Content
```

## 🎓 User Guide

### For Employers

1. **Register** as Employer
2. **Post Jobs** with required skills
3. **View Candidates** sorted by skill match score
4. **Manage Applications** - change status from Pending → Shortlisted → Accepted
5. **Receive Notifications** when new candidates apply
6. **Filter Candidates** by score to find best matches

### For Candidates

1. **Register** as Candidate
2. **Browse Jobs** and search by keywords
3. **Apply for Jobs** with your skills and cover letter
4. **Track Applications** and view status updates
5. **Receive Notifications** about application status changes

## 🗄️ Database Schema

### Tables

**accounts_customuser**
- user_id (FK to auth_user)
- role (employer/candidate)
- phone
- company_name
- bio
- created_at, updated_at

**jobs_job**
- title
- description
- required_skills
- company_id (FK to accounts_customuser)
- location
- salary_min, salary_max
- experience_level
- job_type
- is_active
- created_at, updated_at

**applications_application**
- job_id (FK to jobs_job)
- candidate_id (FK to accounts_customuser)
- candidate_skills
- cover_letter
- skill_match_score
- status
- resume_url
- applied_at, updated_at
- **unique_together**: (job, candidate)

**notifications_notification**
- user_id (FK to auth_user)
- title
- message
- notification_type
- is_read
- related_application_id (FK)
- created_at

## 🚀 Deployment on PythonAnywhere

### 1. Create PythonAnywhere Account
- Go to pythonanywhere.com
- Sign up for a free account

### 2. Upload Code
```bash
# Clone repository in PythonAnywhere console
git clone <your-repo-url>
```

### 3. Create Virtual Environment
```bash
mkvirtualenv ats_project --python=/usr/bin/python3.8
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Django Settings
- Edit `ats/settings.py`:
  - Change `DEBUG = False`
  - Add your domain to `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']`
  - Set `SECRET_KEY` to a strong value

### 6. Set Up Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Configure Web App
- In PythonAnywhere Web tab:
  - Add new web app
  - Choose Manual configuration
  - Select Python 3.8
  - Point WSGI file to `/path/to/ats/wsgi.py`
  - Set virtualenv to your created environment

### 8. Test & Go Live
- Reload web app
- Visit `yourusername.pythonanywhere.com`

## 📊 Example Workflow

### Scenario: Employer posts job and receives applications

1. **Employer registers** as "Employer" role
2. **Employer posts job**:
   - Title: "Python Developer"
   - Required Skills: "python, django, sql"
   - Location: "Remote"

3. **Candidate registers** as "Candidate"
4. **Candidate applies** with skills: "python, django, postgresql, rest"
5. **System calculates score**: 3 out of 4 skills match = 75%
6. **Employer receives notification** and sees application
7. **Employer changes status** to "shortlisted"
8. **Candidate receives notification** of status update

## 🔒 Security Features

- Django built-in authentication
- CSRF protection on all forms
- Password hashing with PBKDF2
- SQL injection prevention with ORM
- CORS headers configured
- Session-based authentication for APIs

## 📈 Performance

- Database indexing on frequently queried fields
- Pagination to limit result sets
- Select_related and prefetch_related for optimized queries
- Static file caching in production

## 🐛 Troubleshooting

### Migration Errors
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Locked
```bash
rm db.sqlite3
python manage.py migrate
```

## 📝 Project Structure

```
ats_project/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── ats/                    # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/              # User authentication
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── jobs/                  # Job management
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── applications/          # Job applications
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── notifications/         # Notification system
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── jobs.html
│   ├── candidates.html
│   └── notifications.html
└── static/              # CSS, JS files
    ├── css/
    └── js/
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as an ATS Lite system for job management and candidate selection.

## 📞 Support

For questions or issues, please open an issue in the repository.

---

**Happy recruiting! 🎯**
