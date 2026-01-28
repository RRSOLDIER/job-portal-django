from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('recruiter', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/job/create/', views.create_job, name='create_job'),
    path('recruiter/job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('recruiter/application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),


    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),



]
