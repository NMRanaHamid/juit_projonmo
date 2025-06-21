from django.urls import path
from . import views

urlpatterns = [
    path('', views.alumni_directory, name='alumni_directory'),
    path('<int:pk>/', views.alumni_detail, name='alumni_detail'),
]