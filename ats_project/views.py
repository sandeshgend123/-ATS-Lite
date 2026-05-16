from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.models import CustomUser
from jobs.models import Job
from applications.models import Application
from notifications.models import Notification


def index(request):
    """Home page"""
    if request.user.is_authenticated:
        return redirect('/jobs/')
    return redirect('/login/')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/jobs/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        phone = request.POST.get('phone', '')
        company_name = request.POST.get('company_name', '')
        
        # Validation
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create custom user
        CustomUser.objects.create(
            user=user,
            role=role,
            phone=phone,
            company_name=company_name if role == 'employer' else None
        )
        
        # Auto login
        login(request, user)
        return redirect('/jobs/')
    
    return render(request, 'register.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def jobs_list(request):
    """List all jobs with search and filter"""
    jobs = Job.objects.filter(is_active=True).select_related('company')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(required_skills__icontains=search_query)
        )
    
    # Experience level filter
    experience_level = request.GET.get('experience_level', '')
    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)
    
    # Get user role
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        user_role = custom_user.role
    except:
        user_role = None
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search': search_query,
        'experience_level': experience_level,
        'user_role': user_role,
    }
    
    return render(request, 'jobs.html', context)


@login_required(login_url='/login/')
def candidates_list(request):
    """List all applications with scores (for employers)"""
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        if custom_user.role != 'employer':
            return redirect('/jobs/')
    except:
        return redirect('/jobs/')
    
    # Get applications for employer's jobs
    applications = Application.objects.filter(job__company=custom_user).select_related('job', 'candidate')
    
    # Search by job title
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(job__title__icontains=search_query)
    
    # Filter by score range
    min_score = request.GET.get('min_score', '')
    if min_score:
        applications = applications.filter(skill_match_score__gte=int(min_score))
    
    max_score = request.GET.get('max_score', '')
    if max_score:
        applications = applications.filter(skill_match_score__lte=int(max_score))
    
    # Sort by score
    applications = applications.order_by('-skill_match_score')
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'applications': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search': search_query,
        'min_score': min_score,
        'max_score': max_score,
    }
    
    return render(request, 'candidates.html', context)


@login_required(login_url='/login/')
def notifications_view(request):
    """Display notifications"""
    return render(request, 'notifications.html')


@login_required(login_url='/login/')
def job_create(request):
    """Create a new job posting (employer only)"""
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        if custom_user.role != 'employer':
            return redirect('/jobs/')
    except:
        return redirect('/jobs/')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        required_skills = request.POST.get('required_skills')
        location = request.POST.get('location')
        salary_min = request.POST.get('salary_min', 0)
        salary_max = request.POST.get('salary_max', 0)
        experience_level = request.POST.get('experience_level', 'mid')
        job_type = request.POST.get('job_type', 'full-time')
        
        # Validation
        if not all([title, description, required_skills]):
            return render(request, 'job_create.html', {
                'error': 'Please fill in all required fields',
                'form_data': request.POST
            })
        
        try:
            job = Job.objects.create(
                title=title,
                description=description,
                required_skills=required_skills,
                location=location,
                salary_min=int(salary_min) if salary_min else 0,
                salary_max=int(salary_max) if salary_max else 0,
                experience_level=experience_level,
                job_type=job_type,
                company=custom_user,
                is_active=True
            )
            return redirect(f'/jobs/{job.id}/')
        except Exception as e:
            return render(request, 'job_create.html', {
                'error': f'Error creating job: {str(e)}',
                'form_data': request.POST
            })
    
    context = {
        'experience_levels': ['junior', 'mid', 'senior'],
        'job_types': ['full-time', 'part-time', 'contract', 'freelance'],
    }
    return render(request, 'job_create.html', context)


@login_required(login_url='/login/')
def job_detail(request, job_id):
    """View details of a specific job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user already applied
    user_applied = False
    user_application = None
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        if custom_user.role == 'candidate':
            user_application = Application.objects.filter(job=job, candidate=custom_user).first()
            user_applied = user_application is not None
    except:
        pass
    
    context = {
        'job': job,
        'user_applied': user_applied,
        'user_application': user_application,
    }
    
    return render(request, 'job_detail.html', context)


@login_required(login_url='/login/')
def profile_view(request):
    """User profile page"""
    try:
        custom_user = CustomUser.objects.get(user=request.user)
    except:
        return redirect('/jobs/')
    
    context = {
        'custom_user': custom_user,
    }
    
    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def admin_applications_view(request):
    """Admin-only view for all applications with Excel and PDF downloads"""
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/jobs/')
    
    # Get all applications with filters
    applications = Application.objects.all().select_related(
        'job', 'candidate', 'candidate__user', 'job__company', 'job__company__user'
    ).order_by('-applied_at')
    
    # Search filter
    search = request.GET.get('search', '')
    if search:
        applications = applications.filter(
            Q(candidate__user__first_name__icontains=search) |
            Q(candidate__user__last_name__icontains=search) |
            Q(candidate__user__email__icontains=search) |
            Q(job__title__icontains=search)
        )
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Score filter
    min_score = request.GET.get('min_score', '')
    max_score = request.GET.get('max_score', '')
    if min_score:
        applications = applications.filter(skill_match_score__gte=int(min_score))
    if max_score:
        applications = applications.filter(skill_match_score__lte=int(max_score))
    
    # Pagination
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    is_paginated = paginator.num_pages > 1
    
    # Get status choices for filter dropdown
    status_choices = Application._meta.get_field('status').choices
    
    context = {
        'applications': page_obj,
        'is_paginated': is_paginated,
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'min_score': min_score,
        'max_score': max_score,
        'status_choices': status_choices,
    }
    
    return render(request, 'admin_applications.html', context)
