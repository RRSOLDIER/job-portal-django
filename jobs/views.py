from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .decorators import recruiter_required, candidate_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import UserProfile
from django.contrib import messages
from .models import Job


def home(request):
    featured_jobs = Job.objects.order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'featured_jobs': featured_jobs
    })



@login_required
@recruiter_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'recruiter_dashboard.html', {'jobs': jobs})

@login_required
@recruiter_required
def create_job(request):
    if request.method == 'POST':
        Job.objects.create(
            recruiter=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            job_type=request.POST.get('job_type'),
        )
        return redirect('recruiter_dashboard')

    return render(request, 'create_job.html')

@login_required
@candidate_required
def job_list(request):
    query = request.GET.get('q')
    job_type = request.GET.get('type')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs.order_by('-created_at'), 5)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'job_list.html', {
        'jobs': jobs,
        'query': query,
        'job_type': job_type
    })



@login_required
@candidate_required
def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)

    already_applied = JobApplication.objects.filter(
        candidate=request.user,
        job=job
    ).exists()

    if request.method == 'POST' and not already_applied:
        JobApplication.objects.create(
            candidate=request.user,
            job=job
        )
        return redirect('job_list')

    return render(request, 'job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })

from .models import JobApplication

@login_required
@recruiter_required
def view_applicants(request, job_id):
    job = Job.objects.get(id=job_id, recruiter=request.user)

    applications = JobApplication.objects.filter(job=job)

    return render(request, 'view_applicants.html', {
        'job': job,
        'applications': applications
    })


@login_required
@recruiter_required
def update_application_status(request, application_id):
    application = JobApplication.objects.get(
        id=application_id,
        job__recruiter=request.user
    )

    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.save()
        return redirect('view_applicants', job_id=application.job.id)

    return render(request, 'update_status.html', {
        'application': application
    })

@login_required
@candidate_required
def candidate_dashboard(request):
    applications = JobApplication.objects.filter(
        candidate=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'candidate_dashboard.html', {
        'applications': applications
    })


from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            role = user.userprofile.role
            if role == 'recruiter':
                return redirect('recruiter_dashboard')
            else:
                return redirect('candidate_dashboard')

        messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

