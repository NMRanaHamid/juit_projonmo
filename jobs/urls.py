from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/edit/', views.job_update, name='job_update'),
    path('job/<int:pk>/delete/', views.job_delete, name='job_delete'),
]
