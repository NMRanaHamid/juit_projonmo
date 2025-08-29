from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete_images/', views.delete_images, name='delete_images'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),

]
