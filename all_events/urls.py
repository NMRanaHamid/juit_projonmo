from django.urls import path
from . import views

app_name = 'all_events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    # New URLs
    path('<int:pk>/register/', views.event_register, name='event_register'),
    path('<int:pk>/registered-users/', views.event_registered_users, name='event_registered_users'),
]
