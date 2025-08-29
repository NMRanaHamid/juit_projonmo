from django.urls import path
from . import views

app_name = 'notifications'  # <--- this is crucial

urlpatterns = [
    path('', views.all_notifications, name='all_notifications'),
    path('mark-read/', views.mark_all_notifications_read, name='mark_notifications_read'),
]
